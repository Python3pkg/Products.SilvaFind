from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from ExtensionClass import Base

# Silva
from Products.Silva import SilvaPermissions

class MetadataFieldView(Implicit):
    
    security = ClassSecurityInfo()
    
    def __init__(self, field, searchObject):
        self.field = field
        self.searchObject = searchObject
        self.root = self.searchObject.get_root()
    
    def _getMetadataElement(self):
        collection = self.root.service_metadata.getCollection()
        set = collection[self.field.getMetadataSet()]
        element = getattr(set, self.field.getMetadataId())
        return element

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
        
    def getIndexId(self):
        indexId = createIndexId(self._getMetadataElement())
        return indexId

InitializeClass(MetadataFieldView)
