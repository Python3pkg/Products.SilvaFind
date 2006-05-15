from zope.interface import implements

from Products.SilvaFind.interfaces import IMetadataCriteriaField
from Products.SilvaFind.interfaces import IDateRangeMetadataCriteriaField
from Products.SilvaFind.interfaces import IFullTextCriteriaField
from Products.SilvaFind.interfaces import IResultField

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

class BaseMetadataCriteriaField:

    def __init__(self, metadataSet, metadataId):
        self.metadataSet = metadataSet
        self.metadataId = metadataId

    def getMetadataSet(self):
        return self.metadataSet

    def getMetadataId(self):
        return self.metadataId

    def getName(self):
        return "%s-%s" % (self.getMetadataSet(), self.getMetadataId())

class MetadataCriteriaField(BaseMetadataCriteriaField):
    implements(IMetadataCriteriaField)

class DateRangeMetadataCriteriaField(BaseMetadataCriteriaField):
    implements(IDateRangeMetadataCriteriaField)

class FullTextCriteriaField:
    implements(IFullTextCriteriaField)

    def getName(self):
        return "fulltext"

class ResultField:
    implements(IResultField)
    
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def getColumnId(self):
        return self.id

    def getColumnTitle(self):
        return self.title
