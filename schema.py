from zope.interface import implements

from Products.SilvaFind.interfaces import IMetadataSearchField

class Schema:
    def __init__(self, fields):
        self.fields = fields

    def getFields(self):
        return self.fields

    def hasField(self, name):
        return name in self.getFieldNames()

    def getFieldNames(self):
        return [field.getName() for field in self.getFields()]

class MetadataField:
    implements(IMetadataSearchField)

    def __init__(self, metadataSet, metadataId):
        self.metadataSet = metadataSet
        self.metadataId = metadataId

    def getMetadataSet(self):
        return self.metadataSet

    def getMetadataId(self):
        return self.metadataId

    getName = getMetadataId

class ResultsSchema(Schema):
   pass 


class SearchSchema(Schema):
   pass 
