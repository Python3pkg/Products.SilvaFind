from zope.interface import Interface

class ICriteriaView(Interface):
    '''
    To display a criteria both in view and in edit form. 
    '''
    def getTitle():
        '''returns field title for view'''

    def renderWidget():
        '''returns widget HTML for view'''

    def getValue():
        '''returns stored value for the corresponding field'''
        
class IStoreCriteria(Interface):
    '''
    Stores criteria value in query instance
    '''
    def store():
        '''store value in query'''

class IQueryPart(Interface):
    '''
    To build a ZCatalog query
    '''
    def getIndexId():
        '''returns ZCatalog index id of the criteria'''

    def getValue():
        '''returns value used by catalog searches, could be a dict for
        DateIndex for instance.'''

class IIndexedField(Interface):
    '''
    Check if index corresponding to field in schema is setup.
    '''
    def checkIndex():
        '''checks if a corresponding index exists;
        raise an exception if not
        '''

class ICatalogMetadataSetup(Interface):
    '''
    Setup of metadata columns in Silva catalog
    '''
    def setUp():
        '''
        Setup of metadata columns in Silva catalog
        '''
