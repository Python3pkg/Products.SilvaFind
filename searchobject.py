from ZODB.PersistentMapping import PersistentMapping

class SearchObject:
    def __init__(self, searchSchema=None, resultsSchema=None):
        self.searchSchema = searchSchema
        self.resultsSchema = resultsSchema
        self.searchValues = PersistentMapping()

    def setSearchSchema(self, schema):
        self.searchSchema = schema
        
    def setResultsSchema(self, schema):
        self.resultsSchema = schema

    def getFieldValue(self, name):
        if self.searchSchema:
            searchSchema = self.searchSchema
            if searchSchema.hasField(name):
                return self.searchValues.get(name, None)
        raise AttributeError(name)
        
    def setFieldValue(self, name, value):
        if self.searchSchema:
            searchSchema = self.searchSchema
            if searchSchema.hasField(name):
                self.searchValues[name] = value
        
