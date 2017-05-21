# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 Infrae. All rights reserved.
# See also LICENSE.txt

import unittest

from zope.component import queryMultiAdapter
from zope.interface.verify import verifyObject
from zeam.utils.batch import Batch

from Products.Silva.testing import TestRequest
from Products.SilvaFind import schema
from Products.SilvaFind.interfaces import IResultField, IResultView
from Products.SilvaFind.testing import FunctionalLayer


class ResultTestCase(unittest.TestCase):
    """Test some silva find features.
    """
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('author')

        factory = self.root.manage_addProduct['SilvaFind']
        factory.manage_addSilvaFind('search', 'Search your Site')
        factory = self.root.manage_addProduct['Silva']
        factory.manage_addFolder('folder', 'Folder')
        factory = self.root.folder.manage_addProduct['Silva']
        factory.manage_addMockupVersionedContent('info', 'Information')

        self.documents = Batch(
            self.root.service_catalog(
                meta_type=['Mockup VersionedContent'], path='/root/folder'))
        self.empty = Batch([])

    def test_date(self):
        result = schema.DateResultField('date', 'Publication Date')
        self.assertTrue(verifyObject(IResultField, result))
        self.assertEqual(result.getName(), 'publicationdate')
        self.assertEqual(result.getId(), 'date')
        self.assertEqual(result.getTitle(), 'Publication Date')
        self.assertEqual(result.getDescription(), '')

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))
        view.update(self.documents)
        # XXX difficult to test, contain a date
        self.assertNotEqual(view.render(self.documents[0]), '')

    def test_metatype(self):
        result = schema.MetatypeResultField('icon', 'Icon')
        self.assertTrue(verifyObject(IResultField, result))
        self.assertEqual(result.getName(), 'icon')
        self.assertEqual(result.getId(), 'icon')
        self.assertEqual(result.getTitle(), 'Icon')
        self.assertEqual(result.getDescription(), '')

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))

        view.update(self.documents)
        self.assertEqual(
            view.render(self.documents[0]),
            '<img height="16" width="16" '
            'src="http://localhost/root/++resource++icon-Mockup-VersionedContent.png" '
            'alt="Mockup VersionedContent" />')

    def test_link(self):
        result = schema.LinkResultField('link', 'Link to result')
        self.assertTrue(verifyObject(IResultField, result))
        self.assertEqual(result.getName(), 'linktoresult')
        self.assertEqual(result.getId(), 'link')
        self.assertEqual(result.getTitle(), 'Link to result')
        self.assertEqual(result.getDescription(), '')

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))

        view.update(self.documents)
        self.assertEqual(
            view.render(self.documents[0]),
            '<a href="http://localhost/root/folder/info" '
            'class="searchresult-link">info</a>')

    def test_thumbnail(self):
        result = schema.ThumbnailResultField(
            'thumb', 'Image Thumbnail', 'Small version of the image')
        self.assertTrue(verifyObject(IResultField, result))
        self.assertEqual(result.getName(), 'imagethumbnail')
        self.assertEqual(result.getId(), 'thumb')
        self.assertEqual(result.getTitle(), 'Image Thumbnail')
        self.assertEqual(result.getDescription(), 'Small version of the image')

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))

        view.update(self.documents)
        self.assertEqual(
            view.render(self.documents[0]), None)

    def test_breadcrumbs(self):
        result = schema.BreadcrumbsResultField('breadcrumbs', 'Breadcrumbs')
        self.assertTrue(verifyObject(IResultField, result))

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))

        view.update(self.documents)
        # XXX This fails because request is a TestRequest, so we don't
        # have the same absolute_url
        self.assertEqual(
            view.render(self.documents[0]),
            '<span class="searchresult-breadcrumb">'
            '<a href="http://localhost/root">root</a>'
            '<span> &#183; </span>'
            '<a href="http://localhost/root/folder">Folder</a></span>')

    def test_metadata(self):
        result = schema.MetadataResultField(
            'silva-extra:creator', 'Creator', 'Content creator')
        self.assertTrue(verifyObject(IResultField, result))
        self.assertEqual(result.getName(), 'creator')
        self.assertEqual(result.getId(), 'silva-extra:creator')
        self.assertEqual(result.getTitle(), 'Creator')
        self.assertEqual(result.getDescription(), 'Content creator')

        view = queryMultiAdapter(
            (result, self.root.search, TestRequest()), IResultView)
        self.assertTrue(verifyObject(IResultView, view))

        view.update(self.documents)
        self.assertEqual(
            view.render(self.documents[0]),
            '<span class="searchresult-field metadata-silva-extra-creator">'
            '<span class="searchresult-field-title">Creator</span>'
            '<span class="searchresult-field-value">author</span></span>')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResultTestCase))
    return suite
