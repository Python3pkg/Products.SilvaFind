# Copyright (c) 2006-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest
import DateTime
import SilvaFindTestCase
from Products.SilvaFind.globalschema import globalSearchFields



class SilvaQueryTestCase(SilvaFindTestCase.SilvaFindTestCase):

    def afterSetUp(self):
        self.add_query(self.root, 'query', 'Query')

    def test_instance(self):
        self.failUnless('query' in self.root.objectIds())

    def test_edit(self):
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

    def test_search(self):
        document = self.add_document(self.root, 'doc', 'Document')
        document.get_editable().content.manage_edit(u'<p>abc def xyz</p>')
        document.set_unapproved_version_publication_datetime(DateTime.DateTime())
        document.approve_version()
        query = self.root.query
        request = query.REQUEST
        request.set('fulltext', 'xyz')
        query._edit(request)
        resultBrains = query.searchResults()
        self.assertEquals(len(resultBrains), 1)
        resultObjects = [result.getObject().object() for result in resultBrains]
        self.failUnless(document in resultObjects)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaQueryTestCase))
    return suite
