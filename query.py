from ZODB.PersistentMapping import PersistentMapping
from schema import globalSearchSchema
from schema import globalResultsSchema

class Query:
    def __init__(self):
        self.searchValues = PersistentMapping()
    
    def getSearchSchema(self):
        return globalSearchSchema
    
    def getResultsSchema(self):
        return globalResultsSchema
    
    searchSchema=property(getSearchSchema, None, None,
        "access to the instance search schema")
    
    resultsSchema=property(getResultsSchema, None, None,
        "access to the instance search schema")
    
    def getCriteriaValue(self, name):
        if self.searchSchema:
            searchSchema = self.searchSchema
            if searchSchema.hasField(name):
                return self.searchValues.get(name, None)
        raise AttributeError(name)
        
    def setCriteriaValue(self, name, value):
        if self.searchSchema:
            searchSchema = self.searchSchema
            if searchSchema.hasField(name):
                self.searchValues[name] = value

    def getResultsColumnIds(self):
        return [field.getColumnId() 
            for field in self.resultsSchema.getFields()]
           
