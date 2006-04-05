from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions

# SilvaFind
from Products.SilvaFind.adapters.criteria import CriteriaStorage
from Products.SilvaFind.adapters.criteria import SilvaFindError

class FullTextCriteriaStorage(CriteriaStorage):
    def store(self):
        REQUEST = self.query.REQUEST
        field_name = self.criteria.getName()
        if hasattr(REQUEST, field_name):
            criteria_value = getattr(REQUEST, field_name)
            self.query.setCriteriaValue(field_name, criteria_value)

class FullTextCriteriaView(Implicit):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criteria, query):
        self.criteria = criteria
        self.query = query
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self):
        value = self.getValue()
        if value is None:
            value = ""
        html = '''
        <input type="text" name="%s" value="%s" /> 
        '''
        return html % (self.criteria.getName(), value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        value = self.query.getCriteriaValue(self.criteria.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return 'Full text'
        
    def getIndexId(self):
        return 'fulltext'

InitializeClass(FullTextCriteriaView)

class IndexedFullTextCriteria:
    def __init__(self, criteria, root):
        self.criteria = criteria
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'fulltext'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
