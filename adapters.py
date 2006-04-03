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
        value = self.searchObject.getCriteriaValue(element.field.getId())
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

