from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from ExtensionClass import Base

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaMetadata.Index import createIndexId

class SilvaFindError(Exception):
    pass

class MetadataFieldRoot:
    def __init__(self, field, root):
        self.field = field
        self.root = root

    def _getMetadataElement(self):
        collection = self.root.service_metadata.getCollection()
        set = collection[self.field.getMetadataSet()]
        element = getattr(set, self.field.getMetadataId())
        return element

    def getIndexId(self):
        indexId = createIndexId(self._getMetadataElement())
        return indexId

class MetadataFieldView(Implicit, MetadataFieldRoot):
    
    security = ClassSecurityInfo()
    
    def __init__(self, field, searchObject):
        root = searchObject.get_root()
        MetadataFieldRoot.__init__(self, field, root)
        self.searchObject = searchObject
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self):
        element = self._getMetadataElement()
        value = self.getValue()
        return element.field.render(value)

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        element = self._getMetadataElement()
        value = self.searchObject.getCriteriaValue(self.field.getName())
        return value
        
    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        element = self._getMetadataElement()
        return element.Title()
        
InitializeClass(MetadataFieldView)


class MetadataIndexedField(MetadataFieldRoot):
    def __init__(self, field, root):
        MetadataFieldRoot.__init__(self, field, root)
        self.catalog = root.service_catalog

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)

            
class Storage:
    def __init__(self, field, searchObject):
        self.field = field
        self.searchObject = searchObject
        
class MetadataFieldStorage(Storage):
    def store(self):
        REQUEST = self.searchObject.REQUEST
        set_name = self.field.getMetadataSet()
        field_name = self.field.getMetadataId()
        if hasattr(REQUEST, set_name):
            set_values = getattr(REQUEST, set_name)
            if set_values.has_key(field_name):
                field_value = set_values[field_name]
                self.searchObject.setCriteriaValue(field_name, field_value)

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


class CatalogMetadataSetup:
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)
