from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions

# SilvaFind
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError

class StoreMetatypeCriterion(StoreCriterion):
    def store(self, REQUEST):
        #XXX some room for refactoring here
        field_name = self.criterion.getName()
        criterion_value = REQUEST.get(field_name, None)
        if criterion_value is None:
            return
        self.query.setCriterionValue(field_name, criterion_value)

class MetatypeCriterionView(Implicit):
    
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

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderPublicWidget')
    def renderPublicWidget(self):
        value = self.getValue(self.query.REQUEST)
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        if value is None:
            value = ""
        html = '<select multiple="1" name="%s:list" id="%s" size="5"         style="width: 100%%" > ' % (self.criterion.getName(),
                            self.criterion.getName())
        meta_types = []
        for meta_type in self.query.REQUEST.model.service_catalog.uniqueValuesFor(self.getIndexId()):
            selected = ''
            if meta_type in value:
                selected = ' selected="true"'
            meta_types.append('<option value="%s"%s>%s</option>' % (meta_type, selected, meta_type))
        html += '\n'.join(meta_types) 
        html += '</select>'
        return html 
    
    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value = REQUEST.get(field_name, None)
        if value:
            if type(value) != type([]):
                value = unicode(value, 'UTF-8')
            else:
                values = []
                for vl in value:
                    values.append(unicode(vl, 'UTF-8'))
                value = values
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
        return 'content type'
        
    def getIndexId(self):
        return 'meta_type'

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        return 'The Content Type of the object(s).'

InitializeClass(MetatypeCriterionView)

class IndexedMetatypeCriterion:
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'meta_type'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
