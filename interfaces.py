from zope.interface import Interface

'''
A query is a set of criteria.
A criteria is made both of an indexed field of content items
and of value(s) that will be searched for in the catalog.
'''

class ISilvaQuery(Interface):
    '''Persistent query'''
    def get_root():
        '''returns the Silva Root under which the object is stored'''

    def getCriteriaValue(schemaField):
        '''returns stored value for schemaField'''

class IMetadataCriteriaField(Interface):
    '''
    Criteria corresponding to indexed SilvaMetadata fields
    '''
    def getMetadataSet():
        '''returns Silva MetadataSet id'''
        
    def getMetadataId():
        '''returns Silva MetadataSet element id'''

class IDateRangeMetadataCriteriaField(IMetadataCriteriaField):
    '''
    Criteria corresponding to indexed SilvaMetadata fields
    date
    '''

class IFullTextCriteriaField(Interface):
    '''
    Criteria corresponding to the Silva full text index
    '''

class IResultField(Interface):
    '''
    Mapping between schema results field and ZCatalog metadata column
    '''
    def getColumnId():
        '''returns catalog column id
        '''
