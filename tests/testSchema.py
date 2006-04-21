from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import MetadataCriteriaField
from Products.SilvaFind.query import Query
from Products.SilvaFind.errors import SilvaFindError

class testSchema(TestCase):

    def setUp(self):
        self.field1 = MetadataCriteriaField('meta-set', 'field-id1')
        self.field2 = MetadataCriteriaField('meta-set', 'field-id2')
        self.schema = SearchSchema([self.field1, self.field2])

    def testInstanciation(self):
        self.failIf(self.schema is None)

    def testAccessFields(self):
        self.assertEquals([self.field1, self.field2], self.schema.getFields())

    def testFieldNames(self):
        self.assertEquals(['meta-set-field-id1', 'meta-set-field-id2'], self.schema.getFieldNames())

    def testHasField(self):
        self.failIf(self.schema.hasField('meta-set-field-id3'))
        self.failUnless(self.schema.hasField('meta-set-field-id1'))
        
class testMetadataCriteriaField(TestCase):

    def setUp(self):
        self.field = MetadataCriteriaField('meta-set', 'field-id')

    def testInstanciation(self):
        self.failIf(self.field is None)
        self.assertEquals('meta-set', self.field.getMetadataSet())
        self.assertEquals('field-id', self.field.getMetadataId())

class testSearchObject(TestCase):
    def setUp(self):
        self.obj = Query()

    def testGetCriteriaValue(self):
        self.assertEquals(None, self.obj.getCriteriaValue('fulltext'))
        self.assertEquals(None,
        self.obj.getCriteriaValue('silva-content-maintitle'))
        self.assertRaises(SilvaFindError, self.obj.getCriteriaValue, 'xyz')

    def testSetCriteriaValue(self):
        self.obj.setCriteriaValue('fulltext', 1)
        self.assertEquals(1, self.obj.getCriteriaValue('fulltext'))
        self.obj.setCriteriaValue('silva-content-maintitle', '1')
        self.assertEquals('1', self.obj.getCriteriaValue('silva-content-maintitle'))

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(testSchema, 'test'))
    suite.addTest(makeSuite(testMetadataCriteriaField, 'test'))
    suite.addTest(makeSuite(testSearchObject, 'test'))
    return suite
