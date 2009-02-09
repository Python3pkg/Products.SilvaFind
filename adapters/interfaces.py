from zope.interface import Interface

class ICriterionView(Interface):
    '''
    To display a criterion both in view and in edit form.
    '''
    def getTitle():
        '''returns field title for view'''

    def getDescription():
        '''returns description of the criterion field'''

    def canBeShown():
        '''Boolean indicating if show chechbox should be shown in edit view'''

    def renderWidget(value):
        '''returns widget HTML for view'''

    def renderEditWidget():
        '''returns widget HTML rendered with stored value'''

    def renderPublicWidget():
        '''returns widget HTML rendered with value from REQUEST'''

    def getValue(REQUEST):
        '''returns value from REQUEST or stored value'''

    def getStoredValue():
        '''returns stored value for the corresponding field'''

class IStoreCriterion(Interface):
    '''
    Stores criterion value in query instance
    '''
    def store(REQUEST):
        '''store value in query

           REQUEST could be a dict
        '''

class IQueryPart(Interface):
    '''
    To build a ZCatalog query
    '''
    def getIndexId():
        '''returns ZCatalog index id of the criterion'''

    def getIndexValue(REQUEST):
        '''returns value used by catalog searches, could be a dict for
        DateIndex for instance.

        The value in REQUEST is used.
        If not found, stored value is used.
        '''

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

class IResultView(Interface):
    '''
    To display a result both in view and in edit form.
    '''
    def getTitle():
        '''returns field title for view'''

    def getID():
        '''returns id of resultfield
        '''

    def renderWidget(value):
        '''returns widget HTML for view'''

    def renderEditWidget():
        '''returns widget HTML rendered with stored value'''


