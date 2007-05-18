from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions

# SilvaFind
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError

class StorePathCriterion(StoreCriterion):
    def store(self, REQUEST):
        #XXX some room for refactoring here
        field_name = self.criterion.getName()
        criterion_value = REQUEST.get(field_name, None)
        if criterion_value is None:
            return
        sitepath = get_site_path(self.query)
        criterion_value = (sitepath + '/' + criterion_value).replace('//', '/')
        self.query.setCriterionValue(field_name, criterion_value)

def get_site_path(context):
    ppath = list(context.getPhysicalPath())
    vpath = context.virtual_url_path().split('/')
    # remove the siteroot part of the path from the vpath
    # if present
    for path in context.get_root().getPhysicalPath():
        if vpath[0] == path:
            vpath.pop(0)
    vpath.reverse()
    # remove the virtual path entries from the physical
    # path to find the root of the virtual site
    for path in vpath:
        if ppath[-1] == path:
            ppath.pop()
        else:
            break
    return '/'.join(ppath)
    
    
class PathCriterionView(Implicit):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'canBeShown')
    def canBeShown(self):
        return False

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderEditWidget')
    def renderEditWidget(self):
        value = self.getStoredValue() or ''
        sitepath = get_site_path(self.query)
        if value.startswith(sitepath):
            value = value[len(sitepath):]
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        value = self.getValue(self.query.REQUEST) or ''
        sitepath = get_site_path(self.query)
        if value.startswith(sitepath):
            value = value[len(sitepath):]
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        if value is None:
            value = ""
        html = '''
        <input type="text" name="%s" id="%s" value="%s" size="20" class="store" /> 
        '''
        return html % (self.criterion.getName(), 
                       self.criterion.getName(),
                       value)
    
    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value = REQUEST.get(field_name, None)
        if value:
            pass
            # XXX pathindex does not work with unicode, so do not try
        else:
            value = self.getStoredValue()
        if value is None:
            value = ''
        return value
        
    getIndexValue = getValue

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        value = self.query.getCriterionValue(self.criterion.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return 'below path'
        
    def getIndexId(self):
        return 'path'

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        return 'Only search below this location (a path from the site root).'

InitializeClass(PathCriterionView)

class IndexedPathCriterion:
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'path'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
