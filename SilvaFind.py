# Zope
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZODB.PersistentMapping import PersistentMapping

# zope3
from zope.interface import implements
from zope.app import zapi

# Silva
from Products.Silva.Content import Content
from Products.Silva.i18n import translate as _
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit
from Products.Silva import mangle

from Products.SilvaMetadata.Index import createIndexId

#SilvaFind
from Products.SilvaFind.query import Query
from Products.SilvaFind.interfaces import ISilvaQuery
from Products.SilvaFind.adapters.interfaces import ICriterionView
from Products.SilvaFind.adapters.interfaces import IQueryPart
from Products.SilvaFind.adapters.interfaces import IStoreCriterion


icon='www/find.png'

class SilvaFind(Query, Content, SimpleItem):
    __doc__ = _("""This a special document that can show a list of content
       items resulting from a search with specific values for criteria
       or a form to enter search criteria before getting results.""")

    security = ClassSecurityInfo()

    meta_type = "Silva Find"

    implements(ISilvaQuery)

    def __init__(self, id):
        Content.__init__(self, id,
            '[Title is stored in metadata. This is a bug.]')
        Query.__init__(self)
        self.shownFields = PersistentMapping()

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

    security.declareProtected(SilvaPermissions.View, 'getFieldViews')
    def getFieldViews(self):
        result = []
        for field in self.service_find.getSearchSchema().getFields():
            searchFieldView = zapi.getMultiAdapter((field, self), ICriterionView)
            # wrapped to enable security checks
            searchFieldView = searchFieldView.__of__(self)
            result.append(searchFieldView)
        return result  

    security.declareProtected(SilvaPermissions.View, 'getPublicFieldViews')
    def getPublicFieldViews(self):
        result = [view for view in self.getFieldViews()
                    if self.isShown(view.getName())]
        return result  

    security.declareProtected(SilvaPermissions.View, 'isShown')
    def isShown(self, fieldName):
        return self.shownFields.get(fieldName, False)

    security.declareProtected(SilvaPermissions.View, 'isFormNeeded')
    def isFormNeeded(self):
        for value in self.shownFields.values():
            if value:
                return True
        return False

    security.declareProtected(SilvaPermissions.View, 'searchResults')
    def searchResults(self, REQUEST={}):
        catalog = self.get_root().service_catalog
        searchArguments = self.getCatalogSearchArguments(REQUEST)
        searchArguments['version_status'] = ['public']
        results = catalog.searchResults(searchArguments)
        return results

    security.declareProtected(SilvaPermissions.View, 'searchResultsObjects')
    def searchResultsObjects(self, REQUEST={}):
        results = self.searchResults(REQUEST)
        return [result.getObject().get_silva_object() for result in results]
    
    security.declareProtected(SilvaPermissions.View, 'getResultsColumnIds')

    #MUTATORS
    security.declareProtected(SilvaPermissions.ChangeSilvaContent, 'manage_edit')
    def manage_edit(self, REQUEST):
        """Store fields values
        """
        self._edit(REQUEST)
        REQUEST.RESPONSE.redirect(self.absolute_url() + '/edit/tab_edit')

    def _edit(self, REQUEST):
        """Store fields values
        """
        self.storeCriterionValues(REQUEST)
        self.storeShownCriterion(REQUEST)

    #HELPERS
    def storeCriterionValues(self, REQUEST):
        for field in self.getSearchSchema().getFields():
            storeCriterion = zapi.getMultiAdapter((field, self), IStoreCriterion)
            storeCriterion.store(REQUEST)

    def storeShownCriterion(self, REQUEST):
        for field in self.getSearchSchema().getFields():
            fieldName = field.getName()
            self.shownFields[fieldName] = REQUEST.get('show_'+fieldName, False)

    def getCatalogSearchArguments(self, REQUEST):
        searchArguments = {}
        for field in self.getSearchSchema().getFields():
            queryPart = zapi.getMultiAdapter((field, self), IQueryPart)
            value = queryPart.getIndexValue(REQUEST)
            if value is None:
                value = ''
            searchArguments[queryPart.getIndexId()] = value
        return searchArguments

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

