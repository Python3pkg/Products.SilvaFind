from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaMetadata.Index import createIndexId

# SilvaFind
from Products.SilvaFind.adapters.criteria import Storage
from Products.SilvaFind.adapters.criteria import SilvaFindError

class FullTextFieldStorage(Storage):
    def store(self):
        REQUEST = self.searchObject.REQUEST
        field_name = self.field.getName()
        if hasattr(REQUEST, field_name):
            field_value = getattr(REQUEST, field_name)
            self.searchObject.setCriteriaValue(field_name, field_value)

class FullTextFieldView(Implicit):
    
    security = ClassSecurityInfo()
    
    def __init__(self, field, searchObject):
        self.field = field
        self.searchObject = searchObject
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self):
        value = self.getValue()
        if value is None:
            value = ""
        html = '''
        <input type="text" name="%s" value="%s" /> 
        '''
        return html % (self.field.getName(), value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        value = self.searchObject.getCriteriaValue(self.field.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return 'Full text'
        
    def getIndexId(self):
        return 'fulltext'

InitializeClass(FullTextFieldView)

class FullTextIndexedField:
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'fulltext'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
