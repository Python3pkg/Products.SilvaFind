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

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'canBeShown')
    def canBeShown(self):
        return True 
        
    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        element = self._getMetadataElement()
        return element.Description()
    
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

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        # we don't want to show widgets for stored values...
        value = self.getStoredValue()
        if value:
            stored = True
        else:
            stored = False
            value = self.getValue(self.query.REQUEST)
        if stored:
            return self.renderValue(value)
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderValue')
    def renderValue(self, value):
        return "<strong>%s</strong>" % value
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        element = self._getMetadataElement()
        return element.field.render(value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        value = self.getStoredValue()
        if value:
            return value
        set_name = self.criterion.getMetadataSet()
        field_name = self.criterion.getMetadataId()
        set_values = REQUEST.get(set_name, None)
        if set_values:
            value = set_values.get(field_name, None)
        if value:
            value = unicode(value, 'UTF-8')
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
        'renderWidget')
    def renderWidget(self, value):
        if value:
            value_lower, value_upper = value
            if value_lower == None:
                value_lower = ''
            if value_upper == None:
                value_upper = ''
        else:
            value_lower = ''
            value_upper = ''
        widget = """
        <table border="0">
        <tr>
            <td style="border:0;">between</td>
            <td style="border:0;"><input name="%(name)s_lower" value="%(lower)s"/></td>
        </tr>
        <tr>
            <td style="border:0;">and</td>
            <td style="border:0;"><input name="%(name)s_upper" value="%(upper)s"/></td>
        </tr>
        <tr>
            <td style="border:0;"></td>
            <td style="border:0;"><small>* only integers</small></td>
        </tr>
        </table>
        """
        return widget % {'name':self.criterion.getName() , 'lower':value_lower, 'upper':value_upper}

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        # we don't want to show widgets for stored values...
        value = self.getStoredValue()
        if value[0] or value[1]:
            stored = True
        else:
            stored = False
            value = self.getValue(self.query.REQUEST)
        if stored:
            return self.renderValue(value)
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderValue')
    def renderValue(self, value):
        return "<strong>%s - %s</strong>" % value
    
    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value_lower = REQUEST.get(field_name+'_lower', None)
        value_upper = REQUEST.get(field_name+'_upper', None)
        stored_lower, stored_upper = self.getStoredValue()
        if value_lower:
            try:
                value_lower = int(value_lower)
            except:
                value_lower = ''
        if value_upper:
            try:
                value_upper = int(value_upper)
            except:
                value_upper = ''
        if stored_lower:
            if not(value_lower) or value_lower < stored_lower:
                value_lower = stored_lower
        if stored_upper:
            if not(value_upper) or value_upper > stored_upper:
                value_upper = stored_upper
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
                try:
                    upper = int(value_upper)
                except:
                    return {}
                return {'query':upper, 'range':'max'}
        else:
            try:
                lower = int(value_lower)
            except:
                lower = 0
            if not value_upper:
                return {'query':lower, 'range':'min'}
            else:
                try:
                    upper = int(value_upper)
                except:
                    return {'query':lower, 'range':'min'}
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
        'renderWidget')
    def renderWidget(self, value):
        if value:
            value_begin, value_end = value
            if value_begin == None:
                value_begin = ''
            if value_end == None:
                value_end = ''
        else:
            value_begin = ''
            value_end = ''
        widget = """
        <table border="0">
        <tr>
            <td style="border:0;">from</td>
            <td style="border:0;"><input name="%(name)s_begin" id="%(idname)s" value="%(begin)s"/></td>
        </tr>
        <tr>
            <td style="border:0;">to</td>
            <td style="border:0;"><input name="%(name)s_end" value="%(end)s"/></td>
        </tr>
        <tr>
            <td style="border:0;"></td>
            <td style="border:0;"><small>* yyyy/mm/dd</small></td>
        </tr>
        </table>
        """
        return widget % {'name':self.criterion.getName(), 'begin':value_begin, 
                         'end':value_end, 
                         'idname':self.criterion.getName().split('-')[-1]}

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        # we don't want to show widgets for stored values...
        value = self.getStoredValue()
        if value[0] or value[1]:
            stored = True
        else:
            stored = False
            value = self.getValue(self.query.REQUEST)
        if stored:
            return self.renderValue(value)
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderValue')
    def renderValue(self, value):
        return "<strong>%s - %s</strong>" % value

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value_begin = REQUEST.get(field_name+'_begin', None)
        value_end = REQUEST.get(field_name+'_end', None)
        stored_begin, stored_end = self.getStoredValue()
        if value_begin:
            try:
                value_begin = DateTime(value_begin)
            except:
                value_begin = ''
        if value_end:
            try:
                value_end = DateTime(value_end)
            except:
                value_end = ''
        if stored_begin:
            if not(value_begin) or value_begin < stored_begin:
                value_begin = stored_begin
        if stored_end:
            if not(value_end) or value_end > stored_end:
                value_end = stored_end
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
                try:
                    date_end = DateTime(value_end)
                except:
                    return {}
                return {'query':date_end, 'range':'max'}
        else:
            try:
                date_begin = DateTime(value_begin)
            except:
                date_begin = None
            if not value_end:
                return {'query':date_begin, 'range':'min'}
            else:
                try:
                    date_end = DateTime(value_end)
                except:
                    if date_begin:
                        return {'query':date_begin, 'range':'min'}
                    else:
                        return {}
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
