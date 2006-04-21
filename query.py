from ZODB.PersistentMapping import PersistentMapping
from globalschema import globalSearchSchema
from globalschema import globalResultsSchema

from errors import SilvaFindError

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
        searchSchema = self.searchSchema
        if searchSchema.hasField(name):
            return self.searchValues.get(name, None)
        else:
            raise SilvaFindError('No field named %s defined in search schema' %
            name)
        
    def setCriteriaValue(self, name, value):
        searchSchema = self.searchSchema
        if searchSchema.hasField(name):
            self.searchValues[name] = value
        else:
            raise SilvaFindError('No field named %s defined in search schema' %
            name)

    def getResultsColumnIds(self):
        return [field.getColumnId() 
            for field in self.resultsSchema.getFields()]
           
    def getResultsColumnTitles(self):
        return [field.getColumnTitle() 
            for field in self.resultsSchema.getFields()]
           
