# Copyright (c) 2006-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from unittest import TestCase
from unittest import TestSuite
from unittest import makeSuite
from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import MetadataCriterionField
from Products.SilvaFind.query import Query
from Products.SilvaFind.errors import SilvaFindError

class testSchema(TestCase):

    def setUp(self):
        self.field1 = MetadataCriterionField('meta-set', 'field-id1')
        self.field2 = MetadataCriterionField('meta-set', 'field-id2')
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

class testMetadataCriterionField(TestCase):

    def setUp(self):
        self.field = MetadataCriterionField('meta-set', 'field-id')

    def testInstanciation(self):
        self.failIf(self.field is None)
        self.assertEquals('meta-set', self.field.getMetadataSet())
        self.assertEquals('field-id', self.field.getMetadataId())

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(testSchema, 'test'))
    suite.addTest(makeSuite(testMetadataCriterionField, 'test'))
    return suite
