try:
    from App.class_init import InitializeClass # Zope 2.12
except ImportError:
    from Globals import InitializeClass # Zope < 2.12

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaFind.i18n import translate as _

# SilvaFind
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError

class StoreFullTextCriterion(StoreCriterion):
    def store(self, REQUEST):
        field_name = self.criterion.getName()
        criterion_value = unicode(REQUEST.get(field_name, None),'UTF-8')
        if criterion_value is None:
            return
        self.query.setCriterionValue(field_name, criterion_value)

class FullTextCriterionView(Implicit):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'canBeShown')
    def canBeShown(self):
        return True 

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderEditWidget')
    def renderEditWidget(self):
        value = self.getStoredValue()
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        value = self.getValue(self.query.REQUEST)
        return {'name': self.criterion.getName(),
                'field_type': self.__class__.__name__,         
                'value': value,}

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        if value is None:
            value = ""
        html = '''
        <input class="store" type="text" name="%s" id="%s" value="%s" size="20" /> 
        '''
        return html % (self.criterion.getName(),
                       self.criterion.getName(),
                       value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value = REQUEST.get(field_name, None)
        if value:
            value = unicode(value, 'UTF-8')
        else:
            value = self.getStoredValue()
        return value
        
    getIndexValue = getValue
    
    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        value = self.query.getCriterionValue(self.criterion.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return _('full text')
        
    def getIndexId(self):
        return 'fulltext'

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        return _('Search the full text.')
        
    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

InitializeClass(FullTextCriterionView)

class IndexedFullTextCriterion:
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'fulltext'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
