# -*- coding: utf-8 -*-
# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from zope.component import queryMultiAdapter
from zope.interface.verify import verifyObject
from zope.publisher.browser import TestRequest

from Products.SilvaFind import schema
from Products.SilvaFind.interfaces import IResultField, IResultView
from Products.Silva.testing import FunctionalLayer


class ResultTestCase(unittest.TestCase):
    """Test some silva find features.
    """
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('author')
        self.request = TestRequest()
        factory = self.root.manage_addProduct['SilvaFind']
        factory.manage_addSilvaFind('search', 'Search your Site')

    def test_date(self):
        result = schema.DateResultField('date', 'Publication Date')
        self.failUnless(verifyObject(IResultField, result))

        view = queryMultiAdapter(
            (self.root.search, result, self.request), IResultView)
        self.assertNotEqual(view, None)
        self.failUnless(verifyObject(IResultView, view))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResultTestCase))
    return suite
