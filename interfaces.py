from zope.interface import Interface

'''
A query is a set of criteria.
A criterion is made both of an indexed field of content items
and of value(s) that will be searched for in the catalog.
'''

class ISilvaQuery(Interface):
    '''Persistent query'''
    def get_root():
        '''returns the Silva Root under which the object is stored'''

    def getCriterionValue(schemaField):
        '''returns stored value for schemaField'''

class IMetadataCriterionField(Interface):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    '''
    def getMetadataSet():
        '''returns Silva MetadataSet id'''
        
    def getMetadataId():
        '''returns Silva MetadataSet element id'''

class IDateRangeMetadataCriterionField(IMetadataCriterionField):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    date
    '''

class IIntegerRangeMetadataCriterionField(IMetadataCriterionField):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    date
    '''

class IFullTextCriterionField(Interface):
    '''
    Criterion corresponding to the Silva full text index
    '''

class IMetatypeCriterionField(Interface):
    '''
    Criterion corresponding to the Silva Meta Type of an object
    '''   
    
class IResultField(Interface):
    '''
    Mapping between schema results field and ZCatalog metadata column
    '''
    def getColumnTitle():
        '''returns catalog column title
        '''

    def render(item):
        '''renders result field for item
        '''
        