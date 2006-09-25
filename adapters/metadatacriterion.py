from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from DateTime import DateTime

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaMetadata.Index import createIndexId

# SilvaFind
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError

class BaseMetadataCriterion:
    
    security = ClassSecurityInfo()
   
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root

    def _getMetadataElement(self):
        collection = self.root.service_metadata.getCollection()
        set = collection[self.criterion.getMetadataSet()]
        element = getattr(set, self.criterion.getMetadataId())
        return element

    def getIndexId(self):
        indexId = createIndexId(self._getMetadataElement())
        return indexId

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        element = self._getMetadataElement()
        print repr(element), repr(element.description)
        return element.description
    
InitializeClass(BaseMetadataCriterion)

class MetadataCriterionView(Implicit, BaseMetadataCriterion):
    
    security = ClassSecurityInfo()
    
    def __init__(self, criterion, query):
        root = query.get_root()
        BaseMetadataCriterion.__init__(self, criterion, root)
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
        set_name = self.criterion.getMetadataSet()
        field_name = self.criterion.getMetadataId()
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
        value = self.query.getCriterionValue(self.criterion.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        element = self._getMetadataElement()
        return element.Title()
    
InitializeClass(MetadataCriterionView)

class IndexedMetadataCriterion(BaseMetadataCriterion):
    def __init__(self, criterion, root):
        BaseMetadataCriterion.__init__(self, criterion, root)
        self.catalog = root.service_catalog

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
            
class StoreMetadataCriterion(StoreCriterion):
    def store(self, REQUEST):
        set_name = self.criterion.getMetadataSet()
        field_name = self.criterion.getMetadataId()
        set_values = REQUEST.get(set_name, None)
        if set_values is None:
            return
        criterion_value = unicode(set_values.get(field_name, None), 'UTF-8')
        if criterion_value is None:
            return
        self.query.setCriterionValue(self.criterion.getName(), criterion_value)

class IntegerRangeMetadataCriterionView(MetadataCriterionView):
    
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
        value_lower, value_upper = value
        widget = """
        <input name="%(name)s_lower" value="%(lower)s" />&nbsp;-&nbsp;<input
        name="%(name)s_upper" value="%(upper)s" />
        """
        return widget % {'name':self.criterion.getName() , 'lower':value_lower, 'upper':value_upper}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value_lower = REQUEST.get(field_name+'_lower', None)
        value_upper = REQUEST.get(field_name+'_upper', None)
        if value_lower is None and value_upper is None:
            value_lower, value_upper = self.getStoredValue()
        return value_lower, value_upper
   
    def getIndexValue(self, REQUEST):
        value_lower, value_upper = self.getValue(REQUEST)
        return self.constructQuery(value_lower, value_upper)    

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        value = self.query.getCriterionValue(self.criterion.getName())
        if value is None:
            return ("", "")
        else:
            return value
    
    def constructQuery(self, value_lower, value_upper):
        if not value_lower:
            if not value_upper:
                return None
            else:
                upper = int(value_upper)
                return {'query':upper, 'range':'max'}
        else:
            lower = int(value_lower)
            if not value_upper:
                return {'query':lower, 'range':'min'}
            else:
                upper = int(value_upper)
                return {'query':[lower, upper], 'range':'min:max'}

InitializeClass(IntegerRangeMetadataCriterionView)

class StoreIntegerRangeMetadataCriterion(StoreCriterion):
    def store(self, REQUEST):
        field_name = self.criterion.getName()
        criterion_value_lower = REQUEST.get(field_name+'_lower', None)
        criterion_value_upper = REQUEST.get(field_name+'_upper', None)
        if criterion_value_lower is None and criterion_value_upper is None:
            return
        if criterion_value_lower:
            criterion_value_lower = int(criterion_value_lower)
        if criterion_value_upper:
            criterion_value_upper = int(criterion_value_upper)
        self.query.setCriterionValue(self.criterion.getName(),
            (criterion_value_lower, criterion_value_upper))
            
class DateRangeMetadataCriterionView(MetadataCriterionView):
    
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
        <span>from</span>&nbsp;<input name="%(name)s_begin" value="%(begin)s" />
        
        <span>to</span>&nbsp;<input name="%(name)s_end" value="%(end)s" />
        """
        return widget % {'name':self.criterion.getName() , 'begin':value_begin, 'end':value_end}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
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
        value = self.query.getCriterionValue(self.criterion.getName())
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

InitializeClass(DateRangeMetadataCriterionView)

class StoreDateRangeMetadataCriterion(StoreCriterion):
    def store(self, REQUEST):
        field_name = self.criterion.getName()
        criterion_value_begin = REQUEST.get(field_name+'_begin', None)
        criterion_value_end = REQUEST.get(field_name+'_end', None)
        if criterion_value_begin is None and criterion_value_end is None:
            return
        self.query.setCriterionValue(self.criterion.getName(),
            (criterion_value_begin, criterion_value_end))
