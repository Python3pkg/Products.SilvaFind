from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from DateTime import DateTime

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
        value = self.query.getCriteriaValue(self.criteria.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        element = self._getMetadataElement()
        return element.Title()
        
InitializeClass(MetadataCriteriaView)

class DateRangeMetadataCriteriaView(MetadataCriteriaView):
    
    security = ClassSecurityInfo()
   
    def getRange(self):
        value = self.query.getCriteriaValue(self.criteria.getName())
        if value is None:
            return ("", "")
        else:
            return value

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self):
        value_begin, value_end = self.getRange()
        widget = """
        <span>From</span>&nbsp;<input name="%(name)s_begin" value="%(begin)s" />
        
        <span>To</span>&nbsp;<input name="%(name)s_end" value="%(end)s" />
        """
        return widget % {'name':self.criteria.getName() , 'begin':value_begin, 'end':value_end}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        value_begin, value_end = self.getRange()
        if not value_begin:
            if not value_end:
                return None
            else:
                date_end = DateTime(value_end)
                return {'query':date_end, 'range':'max'}
        else:
            date_begin = DateTime(value_begin)
            if not value_end:
                return {'query':date_begin, 'range':'min'}
            else:
                date_end = DateTime(value_end)
                return {'query':[date_begin, date_end], 'range':'min:max'}

InitializeClass(DateRangeMetadataCriteriaView)

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

class StoreDateRangeMetadataCriteria(StoreCriteria):
    def store(self):
        REQUEST = self.query.REQUEST
        field_name = self.criteria.getName()
        criteria_value_begin = getattr(REQUEST, field_name+'_begin', None)
        criteria_value_end = getattr(REQUEST, field_name+'_end', None)
        if criteria_value_begin is None and criteria_value_end is None:
            return
        self.query.setCriteriaValue(self.criteria.getName(),
            (criteria_value_begin, criteria_value_end))
