# Copyright (c) 2006-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Zope 3
from zope.interface.verify import verifyObject

from Products.Silva.tests.SilvaTestCase import SilvaTestCase
from Products.Silva.tests.helpers import publishObject
from Products.SilvaFind.interfaces import IFind
import SilvaFindTestCase


class SilvaQueryTestCase(SilvaTestCase):
    """Test some silva find features.
    """

    def afterSetUp(self):
        self.add_find(self.root, 'query', 'Query')

    def test_find(self):
        self.failUnless('query' in self.root.objectIds())
        verifyObject(IFind, self.root.query)

    def test_widgets(self):
        query = self.root.query
        request = query.REQUEST
        request.set('fulltext', 'xyz')
        request.set('meta_type', 'Olliphant')
        request.set('path', '/')
        request.set('silva-content',
                    {'maintitle':'Title',
                     'shorttitle':'Short'})
        query._edit(request)
        # content type
        self.assertEquals(query.getFieldViews()[0].getStoredValue(), 'Olliphant')
        # fulltext
        self.assertEquals(query.getFieldViews()[1].getStoredValue(), 'xyz')
        # title
        self.assertEquals(query.getFieldViews()[2].getStoredValue(), 'Title')
        # short title
        self.assertEquals(query.getFieldViews()[3].getStoredValue(), 'Short')
        # keywords
        # publication time
        # expiration time
        # below_path
        self.assertEquals(query.getFieldViews()[7].getStoredValue(), '/root/')

import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaQueryTestCase))
    return suite
