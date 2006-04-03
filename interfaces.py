from zope.interface import Interface

class ISearchFieldView(Interface):
    def getTitle():
        '''returns field title for view'''

    def renderWidget():
        '''returns widget HTML for view'''

    def getValue():
        '''returns stored value for the corresponding field'''


class IQueryPart(Interface):
    def getIndexId():
        '''returns ZCatalog index id needed to construct query'''

    def getValue():
        '''returns stored value for the corresponding field'''

class ISearchObject(Interface):
    def get_root():
        '''returns Silva Root where the object is stored'''

    def getCriteriaValue(schemaField):
        '''returns stored value for schemaField'''

class IMetadataSearchField(Interface):
    def getMetadataSet():
        '''returns Silva MetadataSet id'''
        
    def getMetadataId():
        '''returns Silva MetadataSet element id'''

class IIndexedField(Interface):
    def checkIndex():
        '''checks if a corresponding index exists;
        raise an exception if not
        '''
        
        
