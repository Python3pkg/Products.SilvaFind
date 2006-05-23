from ZODB.PersistentMapping import PersistentMapping

from errors import SilvaFindError

class Query:
    def __init__(self):
        self.searchValues = PersistentMapping()
    
    def getSearchSchema(self):
        return self.service_find.getSearchSchema()
    
    def getResultsSchema(self):
        return self.service_find.getResultsSchema()
    
    def getCriteriaValue(self, name):
        searchSchema = self.getSearchSchema()
        if searchSchema.hasField(name):
            return self.searchValues.get(name, None)
        else:
            raise SilvaFindError('No field named %s defined in search schema' %
            name)
        
    def setCriteriaValue(self, name, value):
        searchSchema = self.getSearchSchema()
        if searchSchema.hasField(name):
            self.searchValues[name] = value
        else:
            raise SilvaFindError('No field named %s defined in search schema' %
            name)

    def getResultsColumnIds(self):
        return [field.getColumnId() 
            for field in self.getResultsSchema().getFields()]
           
    def getResultsColumnTitles(self):
        return [field.getColumnTitle() 
            for field in self.getResultsSchema().getFields()]
           
