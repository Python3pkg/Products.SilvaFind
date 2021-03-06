# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import unittest

from Acquisition import aq_chain

from zope.component import queryMultiAdapter
from zope.interface.verify import verifyObject
from silva.core.references.reference import get_content_id

from Products.Silva.testing import TestRequest
from Products.SilvaFind.criterion import criterion
from Products.SilvaFind.testing import FunctionalLayer
from Products.SilvaFind.interfaces import (
    ICriterionField, ICriterionData, ICriterionView)


class CriterionTestCase(unittest.TestCase):
    """Test setup for criterion testing.
    """
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('author')
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')
        factory = self.root.manage_addProduct['SilvaFind']
        factory.manage_addSilvaFind('search', 'Search your site')


class FulltextCriterionTestCase(CriterionTestCase):
    """Test fulltext criterion.
    """

    def test_criterion(self):
        field = criterion.FullTextCriterionField()

        self.assertTrue(verifyObject(ICriterionField, field))
        self.assertEqual(field.getName(), "fulltext")
        self.assertEqual(field.getIndexId(), "fulltext")

    def test_data(self):
        search = self.root.search
        field = criterion.FullTextCriterionField()

        data = queryMultiAdapter((field, search), ICriterionData)
        self.assertTrue(verifyObject(ICriterionData, data))

        data.setValue("I will go into the woods")
        self.assertEqual(data.getValue(), "I will go into the woods")
        # XXX Should I test that here ?
        self.assertTrue("fulltext" in search.searchValues)
        self.assertEqual(
            search.searchValues["fulltext"],
            "I will go into the woods")

        data.setValue(None)
        self.assertEqual(data.getValue(), None)
        self.assertFalse("fulltext" in search.searchValues)

    def test_view(self):
        search = self.root.search
        field = criterion.FullTextCriterionField()
        request = TestRequest()
        data = queryMultiAdapter((field, search), ICriterionData)
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        self.assertEqual(view.canBeShown(), True)
        self.assertEqual(view.getWidgetValue(), None)

        self.assertEqual(view.getIndexId(), "fulltext")
        self.assertEqual(view.getIndexValue(), None)

        self.assertEqual(data.getValue(), None)
        view.saveWidgetValue()
        self.assertEqual(data.getValue(), None)

    def test_view_request_value(self):
        search = self.root.search
        field = criterion.FullTextCriterionField()
        request = TestRequest(form={"fulltext": "Dancing fever"})
        data = queryMultiAdapter((field, search), ICriterionData)
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        self.assertEqual(view.getWidgetValue(), "Dancing fever")

        self.assertEqual(view.getIndexId(), "fulltext")
        self.assertEqual(view.getIndexValue(), "Dancing fever")

        self.assertEqual(data.getValue(), None)
        view.saveWidgetValue()
        self.assertEqual(data.getValue(), "Dancing fever")

    def test_view_default_value(self):
        search = self.root.search
        field = criterion.FullTextCriterionField()
        request = TestRequest(form={"fulltext": ""})
        data = queryMultiAdapter((field, search), ICriterionData)
        data.setValue("Disco night")
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        # This fallback on stored value
        self.assertEqual(view.getWidgetValue(), "Disco night")

        self.assertEqual(view.getIndexId(), "fulltext")
        self.assertEqual(view.getIndexValue(), "Disco night")

        self.assertEqual(data.getValue(), "Disco night")
        view.saveWidgetValue()
        # We didn't have any value in the request so it got deleted
        self.assertEqual(data.getValue(), None)


class PathCriterionTestCase(CriterionTestCase):
    """Test path criterion.
    """

    def test_criterion(self):
        field = criterion.PathCriterionField()

        self.assertTrue(verifyObject(ICriterionField, field))
        self.assertEqual(field.getName(), "path")
        self.assertEqual(field.getIndexId(), "path")

    def test_data(self):
        search = self.root.search
        field = criterion.PathCriterionField()

        data = queryMultiAdapter((field, search), ICriterionData)
        self.assertTrue(verifyObject(ICriterionData, data))

        self.assertRaises(AssertionError, data.setValue, "What ?")
        data.setValue(get_content_id(self.root.folder))
        self.assertEqual(data.getValue(), self.root.folder)
        self.assertEqual(aq_chain(data.getValue()), aq_chain(self.root.folder))

        data.setValue(None)
        self.assertEqual(data.getValue(), None)

    def test_view(self):
        search = self.root.search
        field = criterion.PathCriterionField()
        request = TestRequest()
        data = queryMultiAdapter((field, search), ICriterionData)
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        self.assertEqual(view.canBeShown(), False)

        self.assertEqual(view.getIndexId(), "path")
        self.assertEqual(view.getIndexValue(), None)

        self.assertEqual(data.getValue(), None)
        view.saveWidgetValue()
        self.assertEqual(data.getValue(), None)

    def test_view_default_value(self):
        search = self.root.search
        field = criterion.PathCriterionField()
        request = TestRequest()
        data = queryMultiAdapter((field, search), ICriterionData)
        data.setValue(get_content_id(self.root.folder))
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))

        self.assertEqual(view.getIndexId(), "path")
        self.assertEqual(view.getIndexValue(), '/root/folder')

        self.assertEqual(data.getValue(), self.root.folder)
        view.saveWidgetValue()
        # We didn't have any value in the request so it got deleted
        self.assertEqual(data.getValue(), None)


class MetaTypeCriterionTestCase(CriterionTestCase):
    """Test metatype criterion implementation.
    """

    def test_criterion(self):
        field = criterion.MetatypeCriterionField()

        self.assertTrue(verifyObject(ICriterionField, field))
        self.assertEqual(field.getName(), "meta_type")
        self.assertEqual(field.getIndexId(), "meta_type")

    def test_data(self):
        search = self.root.search
        field = criterion.MetatypeCriterionField()

        data = queryMultiAdapter((field, search), ICriterionData)
        self.assertTrue(verifyObject(ICriterionData, data))

        data.setValue(["Silva Document", "Silva Folder"])
        self.assertEqual(data.getValue(), ["Silva Document", "Silva Folder"])

        # empty string or empty list is like None
        data.setValue('')
        self.assertEqual(data.getValue(), None)
        data.setValue('')
        self.assertEqual(data.getValue(), None)

    def test_view(self):
        search = self.root.search
        field = criterion.MetatypeCriterionField()
        request = TestRequest()
        data = queryMultiAdapter((field, search), ICriterionData)
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        self.assertEqual(view.canBeShown(), True)
        self.assertEqual(view.getWidgetValue(), None)

        self.assertEqual(view.getIndexId(), "meta_type")
        self.assertEqual(view.getIndexValue(), None)

        self.assertEqual(data.getValue(), None)
        view.saveWidgetValue()
        self.assertEqual(data.getValue(), None)

    def test_view_request_value(self):
        search = self.root.search
        field = criterion.MetatypeCriterionField()
        request = TestRequest(
            form={"meta_type": ["Silva Link", "", "Silva Ghost"]})
        data = queryMultiAdapter((field, search), ICriterionData)
        view = queryMultiAdapter((field, search, request), ICriterionView)

        self.assertTrue(verifyObject(ICriterionView, view))
        self.assertEqual(view.getWidgetValue(), ["Silva Link", "Silva Ghost"])

        self.assertEqual(view.getIndexId(), "meta_type")
        self.assertEqual(view.getIndexValue(), ["Silva Link", "Silva Ghost"])

        self.assertEqual(data.getValue(), None)
        view.saveWidgetValue()
        self.assertEqual(data.getValue(), ["Silva Link", "Silva Ghost"])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FulltextCriterionTestCase))
    suite.addTest(unittest.makeSuite(PathCriterionTestCase))
    suite.addTest(unittest.makeSuite(MetaTypeCriterionTestCase))
    return suite
