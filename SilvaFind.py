# Zope
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

# Silva
from Products.Silva.Content import Content
from Products.Silva.i18n import translate as _
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit
from Products.Silva import mangle

#SilvaFind
from Products.SilvaFind.searchobject import SearchObject
from Products.SilvaFind import globalSearchSchema

class SilvaFind(SearchObject, Content, SimpleItem):
    __doc__ = _("""This a special document that can show a list of content
       items resulting from a search with specific values for criteria 
       or a form to enter search criteria before getting results.""")

    security = ClassSecurityInfo()

    meta_type = "Silva Find"

    def __init__(self, id):
        Content.__init__(self, id,
            '[Title is stored in metadata. This is a bug.]')
        SearchObject.__init__(self, globalSearchSchema)

    # ACCESSORS
    security.declareProtected(SilvaPermissions.View, 'is_cacheable')
    def is_cacheable(self):
        """Return true if this document is cacheable.
        That means the document contains no dynamic elements like
        code, toc, etc.
        """
        return 0

    def is_deletable(self):
        """always deletable"""
        return 1

    def can_set_title(self):        
        """always settable"""
        # XXX: we badly need Publishable type objects to behave right.
        return 1

    security.declareProtected(SilvaPermissions.View, 'getSearchFields')
    def getSearchFields(self):
        coll = self.get_root().service_metadata.getCollection()
        result = []
        for field in self.searchSchema.getFields():
            set = coll[field.getMetadataSet()]
            element = getattr(set, field.getMetadataId())
            result.append(element.field)
        return result    


    #MUTATORS
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'manage_edit')
    def manage_edit(self, REQUEST=None):
        """Store fields values
        """
        for field in self.searchSchema.getFields():
            set_name = field.getMetadataSet()
            field_name = field.getMetadataId()
            if hasattr(REQUEST, set_name):
                set_values = getattr(REQUEST, set_name)
                if set_values.has_key(field_name):
                    field_value = set_values[field_name]
                    self.setFieldValue(field_name, field_value)
        REQUEST.RESPONSE.redirect(self.absolute_url() + '/edit/tab_edit')

InitializeClass(SilvaFind)

manage_addSilvaFindForm = PageTemplateFile("www/silvaFindAdd", globals(),
    __name__='manage_addSilvaFindForm')

def manage_addSilvaFind(self, id, title, REQUEST=None):
    """Add a silvasearch."""
    if not mangle.Id(self, id).isValid():
        return
    object = SilvaFind(id)
    self._setObject(id, object)
    object = getattr(self, id)
    object.set_title(title)
    add_and_edit(self, id, REQUEST)
    return ''

