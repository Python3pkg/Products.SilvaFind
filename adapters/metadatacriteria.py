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
    
    security = ClassSecurityInfo()
   
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

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criteria.getName()

InitializeClass(BaseMetadataCriteria)

class MetadataCriteriaView(Implicit, BaseMetadataCriteria):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criteria, query):
        root = query.get_root()
        BaseMetadataCriteria.__init__(self, criteria, root)
        self.query = query
    
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

    security.declareProtected(SilvaPermissions.View,
        'renderWidget')
    def renderWidget(self, value):
        element = self._getMetadataElement()
        return element.field.render(value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        set_name = self.criteria.getMetadataSet()
        field_name = self.criteria.getMetadataId()
        set_values = REQUEST.get(set_name, None)
        if set_values is None:
            return
        value = set_values.get(field_name, None)
        if value is None:
            value = self.getStoredValue()
        return value
        
    getIndexValue = getValue
    
    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
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
    def store(self, REQUEST):
        set_name = self.criteria.getMetadataSet()
        field_name = self.criteria.getMetadataId()
        set_values = REQUEST.get(set_name, None)
        if set_values is None:
            return
        criteria_value = set_values.get(field_name, None)
        if criteria_value is None:
            return
        self.query.setCriteriaValue(self.criteria.getName(), criteria_value)

class DateRangeMetadataCriteriaView(MetadataCriteriaView):
    
    security = ClassSecurityInfo()
   
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
        value_begin, value_end = value
        widget = """
        <span>From</span>&nbsp;<input name="%(name)s_begin" value="%(begin)s" />
        
        <span>To</span>&nbsp;<input name="%(name)s_end" value="%(end)s" />
        """
        return widget % {'name':self.criteria.getName() , 'begin':value_begin, 'end':value_end}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criteria.getName()
        value_begin = REQUEST.get(field_name+'_begin', None)
        value_end = REQUEST.get(field_name+'_end', None)
        if value_begin is None and value_end is None:
            value_begin, value_end = self.getStoredValue()
        return value_begin, value_end
   
    def getIndexValue(self, REQUEST):
        value_begin, value_end = self.getValue(REQUEST)
        return self.constructQuery(value_begin, value_end)    

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        value = self.query.getCriteriaValue(self.criteria.getName())
        if value is None:
            return ("", "")
        else:
            return value
    
    def constructQuery(self, value_begin, value_end):
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
class StoreDateRangeMetadataCriteria(StoreCriteria):
    def store(self, REQUEST):
        field_name = self.criteria.getName()
        criteria_value_begin = REQUEST.get(field_name+'_begin', None)
        criteria_value_end = REQUEST.get(field_name+'_end', None)
        if criteria_value_begin is None and criteria_value_end is None:
            return
        self.query.setCriteriaValue(self.criteria.getName(),
            (criteria_value_begin, criteria_value_end))
