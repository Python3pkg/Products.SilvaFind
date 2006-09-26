from zope.interface import implements

from Products.Silva.ViewCode import ViewCode
from Products.SilvaFind.interfaces import IMetadataCriterionField
from Products.SilvaFind.interfaces import IDateRangeMetadataCriterionField
from Products.SilvaFind.interfaces import IIntegerRangeMetadataCriterionField
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

class IntegerRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(IIntegerRangeMetadataCriterionField)

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

    def render(self, context, item):
        return getattr(item.getObject(), self.id)()
    
class MetatypeResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        return context.render_icon_by_meta_type(getattr(item.getObject().object(), 'meta_type'))
    
class MetadataResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        binding = context.service_metadata.getMetadata(item.getObject())
        set, element = self.id.split(':')
        return binding.get(set, element)
    