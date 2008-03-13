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

        self.assertEquals(query.getFieldViews()[0].getStoredValue(), 'Olliphant')
        self.assertEquals(query.getFieldViews()[1].getStoredValue(), 'xyz')
        self.assertEquals(query.getFieldViews()[2].getStoredValue(), 'Title')
        self.assertEquals(query.getFieldViews()[3].getStoredValue(), 'Short')
        self.assertEquals(query.getFieldViews()[6].getStoredValue(), '/root/')
        
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
