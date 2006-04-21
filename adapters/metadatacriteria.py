from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaMetadata.Index import createIndexId

# SilvaFind
from Products.SilvaFind.adapters.criteria import StoreCriteria
from Products.SilvaFind.errors import SilvaFindError

class BaseMetadataCriteria:
    def __init__(self, criteria, root):
        self.criteria = criteria
        self.root = root

    def _getMetadataElement(self):
        collection = self.root.service_metadata.getCollection()
        set = collection[self.criteria.getMetadataSet()]
        element = getattr(set, self.criteria.getMetadataId())
        return element

    def getIndexId(self):
        indexId = createIndexId(self._getMetadataElement())
        return indexId

class MetadataCriteriaView(Implicit, BaseMetadataCriteria):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criteria, query):
        root = query.get_root()
        BaseMetadataCriteria.__init__(self, criteria, root)
        self.query = query
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self):
        element = self._getMetadataElement()
        value = self.getValue()
        return element.field.render(value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        element = self._getMetadataElement()
        value = self.query.getCriteriaValue(self.criteria.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        element = self._getMetadataElement()
        return element.Title()
        
InitializeClass(MetadataCriteriaView)


class IndexedMetadataCriteria(BaseMetadataCriteria):
    def __init__(self, criteria, root):
        BaseMetadataCriteria.__init__(self, criteria, root)
        self.catalog = root.service_catalog

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
            
class StoreMetadataCriteria(StoreCriteria):
    def store(self):
        REQUEST = self.query.REQUEST
        set_name = self.criteria.getMetadataSet()
        field_name = self.criteria.getMetadataId()
        set_values = getattr(REQUEST, set_name, None)
        if set_values is None:
            return
        criteria_value = set_values.get(field_name, None)
        if criteria_value is None:
            return
        self.query.setCriteriaValue(self.criteria.getName(), criteria_value)

