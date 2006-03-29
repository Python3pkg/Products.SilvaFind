from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import MetadataField
from Products.SilvaFind.searchobject import SearchObject

class testSchema(TestCase):

    def setUp(self):
        self.field1 = MetadataField('meta-set', 'field-id1')
        self.field2 = MetadataField('meta-set', 'field-id2')
        self.schema = SearchSchema([self.field1, self.field2])

    def testInstanciation(self):
        self.failIf(self.schema is None)

    def testAccessFields(self):
        self.assertEquals([self.field1, self.field2], self.schema.getFields())

    def testFieldNames(self):
        self.assertEquals(['field-id1', 'field-id2'], self.schema.getFieldNames())

    def testHasField(self):
        self.failIf(self.schema.hasField('field-id3'))
        self.failUnless(self.schema.hasField('field-id1'))
        
class testMetadataField(TestCase):

    def setUp(self):
        self.field = MetadataField('meta-set', 'field-id')

    def testInstanciation(self):
        self.failIf(self.field is None)
        self.assertEquals('meta-set', self.field.getMetadataSet())
        self.assertEquals('field-id', self.field.getMetadataId())

class testSearchObject(TestCase):
    def setUp(self):
        self.field1 = MetadataField('meta-set', 'foo')
        self.field2 = MetadataField('meta-set', 'bar')
        self.schema = SearchSchema([self.field1, self.field2])
        self.obj = SearchObject(self.schema)

    def testGetAttr(self):
        self.assertEquals(None, self.obj.getFieldValue('foo'))
        self.assertEquals(None, self.obj.getFieldValue('bar'))
        self.assertRaises(AttributeError, self.obj.getFieldValue, 'xyz')

    def testSetAttr(self):
        self.obj.setFieldValue('foo', 1)
        self.assertEquals(1, self.obj.getFieldValue('foo'))
        self.obj.setFieldValue('bar', '1')
        self.assertEquals('1', self.obj.getFieldValue('bar'))

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(testSchema, 'test'))
    suite.addTest(makeSuite(testMetadataField, 'test'))
    suite.addTest(makeSuite(testSearchObject, 'test'))
    return suite
