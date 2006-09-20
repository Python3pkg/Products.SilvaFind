from zope.interface import implements

from Products.SilvaFind.interfaces import IMetadataCriterionField
from Products.SilvaFind.interfaces import IDateRangeMetadataCriterionField
from Products.SilvaFind.interfaces import IFullTextCriterionField
from Products.SilvaFind.interfaces import IResultField
from Products.SilvaFind.interfaces import IMetatypeCriterionField

class Schema:
    def __init__(self, fields):
        self.fields = fields

    def getFields(self):
        return self.fields

    def hasField(self, name):
        return name in self.getFieldNames()

    def getFieldNames(self):
        return [field.getName() for field in self.getFields()]

class SearchSchema(Schema):
   pass 

class ResultsSchema(Schema):
   pass 

class BaseMetadataCriterionField:

    def __init__(self, metadataSet, metadataId):
        self.metadataSet = metadataSet
        self.metadataId = metadataId

    def getMetadataSet(self):
        return self.metadataSet

    def getMetadataId(self):
        return self.metadataId

    def getName(self):
        return "%s-%s" % (self.getMetadataSet(), self.getMetadataId())

class MetadataCriterionField(BaseMetadataCriterionField):
    implements(IMetadataCriterionField)

class DateRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(IDateRangeMetadataCriterionField)

class FullTextCriterionField:
    implements(IFullTextCriterionField)

    def getName(self):
        return "fulltext"

class MetatypeCriterionField:
    implements(IMetatypeCriterionField)
    
    def getName(self):
        return "meta_type"
    
class ResultField:
    implements(IResultField)
    
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def getColumnId(self):
        return self.id

    def getColumnTitle(self):
        return self.title
