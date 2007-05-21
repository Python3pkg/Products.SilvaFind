# Zope
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo, getSecurityManager
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZODB.PersistentMapping import PersistentMapping
from Products.ZCTextIndex.ParseTree import ParseError
from ZTUtils import Batch

# zope3
from zope.interface import implements
from zope.app import zapi

# Silva
from Products.Silva.Content import Content
from Products.Silva.i18n import translate as _
from zope.i18n import translate
from Products.Silva import SilvaPermissions
from Products.Silva.helpers import add_and_edit
from Products.Silva import mangle

from Products.SilvaMetadata.Index import createIndexId

#SilvaFind
from Products.SilvaFind.query import Query
from Products.SilvaFind.interfaces import ISilvaQuery
from Products.SilvaFind.adapters.interfaces import ICriterionView
from Products.SilvaFind.adapters.interfaces import IResultView
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
        Content.__init__(self, id)
        Query.__init__(self)
        self.shownFields = PersistentMapping()
        self.shownResultsFields = PersistentMapping()
        # by default we only show fulltext search
        # and a couple of resultfields
        self.shownFields['fulltext'] = True 
        self.shownResultsFields['link'] = True 
        self.shownResultsFields['ranking'] = True 
        self.shownResultsFields['resultcount'] = True 
        self.shownResultsFields['icon'] = True 
        self.shownResultsFields['date'] = True 
        self.shownResultsFields['textsnippet'] = True 
        self.shownResultsFields['thumbnail'] = True 
        self.shownResultsFields['breadcrumbs'] = True 

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
                    if self.isCriterionShown(view.getName())]
        return result  

    security.declareProtected(SilvaPermissions.View, 'isCriterionShown')
    def isCriterionShown(self, fieldName):
        return self.shownFields.get(fieldName, False)

    security.declareProtected(SilvaPermissions.View, 'isResultShown')
    def isResultShown(self, fieldName):
        return self.shownResultsFields.get(fieldName, False)

    security.declareProtected(SilvaPermissions.View, 'isFormNeeded')
    def isFormNeeded(self):
        for value in self.shownFields.values():
            if value:
                return True
        return False

    security.declareProtected(SilvaPermissions.View, 'searchResults')
    def searchResults(self, REQUEST={}):
        # this is here for backwards compatibility
        return self.searchResultsWithDescription(REQUEST)[0]

    security.declareProtected(SilvaPermissions.View,
                             'searchResultsWithDescription')
    def searchResultsWithDescription(self, REQUEST={}):
        catalog = self.get_root().service_catalog
        searchArguments = self.getCatalogSearchArguments(REQUEST)
        searchArguments['version_status'] = ['public']
        query = searchArguments.get('fulltext', '').strip()
        if query and query[0] in ['?', '*']:
            return ([], _('Search query can not start with wildcard character.'))
        try:
            results = catalog.searchResults(searchArguments)
        except ParseError, err:
            return ([], _('Search query contains only common or reserved words.'))

        if not results:
            return ([], _('No items matched your search.'))
        
        # XXX the searchresults could have textsnippets of documents 
        # that the user is not supposed to see. 
        # Instead of filtering these objects out (bad performance)
        # or filtering them out in the getBatch method (screws up resultcount)
        # it is now checked in the pagetemplate with the isViewableForUser

        return (results, '')

    security.declareProtected(SilvaPermissions.View, 'isViewableForUser')
    def isViewableForUser(self, brain):
        security_manager = getSecurityManager()
        return security_manager.checkPermission('View', brain.getObject())

    security.declareProtected(SilvaPermissions.View, 'getBatch')
    def getBatch(self,results, size=20, orphan=2, overlap=0):
        # Custom getabatch method to filter out unviewable objects.
        # This may lead to performance problems because all objects 
        # in the search results need to be accessed until the right
        # number of objects are found.
        # This behaviour also has the sideeffect that the total result 
        # count might change as a user is viewing subsequent batches.
        
        REQ = self.REQUEST


        try:
            start_val = REQ.get('batch_start', '0')
            start = int(start_val)
            size = int(REQ.get('batch_size',size))
        except ValueError:
            start = 0

        result_count = start + size
        filtered_results = []
        index = 0
        for brain in results:
            if self.isViewableForUser(brain):
                filtered_results.append(brain)
                result_count -= 1
            if result_count == 0:
                break
            index += 1
        results = filtered_results + results[index:]

        batch = Batch(results, size, start, 0, orphan, overlap)
        batch.total = len(results)

        def getBatchLink(qs, new_start):
            if new_start is not None:
                if not qs:
                    qs = 'batch_start=%d' % new_start
                elif qs.startswith('batch_start='):
                    qs = qs.replace('batch_start=%s' % start_val,
                                    'batch_start=%d' % new_start)
                elif qs.find('&batch_start=') != -1:
                    qs = qs.replace('&batch_start=%s' % start_val,
                                    '&batch_start=%d' % new_start)
                else:
                    qs = '%s&batch_start=%d' % (qs, new_start)

                return qs

        # create a new query string with the correct batch_start/end 
        # for the next/previous batch

        if batch.end < len(results):
            qs = getBatchLink(REQ.QUERY_STRING, batch.end)
            REQ.set('next_batch_url', '%s?%s' % (REQ.URL, qs))

        if start > 0:
            new_start = start - size
            if new_start < 0: new_start = 0
            qs = getBatchLink(REQ.QUERY_STRING, new_start)
            REQ.set('previous_batch_url', '%s?%s' % (REQ.URL, qs))

        return batch
        
    security.declareProtected(SilvaPermissions.View, 'getResultFieldViews')
    def getResultFieldViews(self):
        result = []
        for field in self.service_find.getResultsSchema().getFields():
            resultFieldView = zapi.getMultiAdapter((field, self), IResultView)
            # wrapped to enable security checks
            resultFieldView = resultFieldView.__of__(self)
            result.append(resultFieldView)
        return result  

    def getPublicResultFieldViews(self):
        result = [view for view in self.getResultFieldViews()
                    if self.isResultShown(view.getName())]
        return result  

    security.declareProtected(SilvaPermissions.View, 'getResultColumns')
    def getResultColumns(self):
        return [(field.getColumnTitle(), field.render) for field in self.getResultsSchema().getFields()]
        
    security.declareProtected(SilvaPermissions.View, 'searchResultsObjects')
    def searchResultsObjects(self, REQUEST={}):
        results = self.searchResults(REQUEST)
        return [result.getObject().get_silva_object() for result in results]
    

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
        self.storeShownResult(REQUEST)

    #HELPERS
    def storeCriterionValues(self, REQUEST):
        for field in self.getSearchSchema().getFields():
            storeCriterion = zapi.getMultiAdapter((field, self), IStoreCriterion)
            storeCriterion.store(REQUEST)

    def storeShownCriterion(self, REQUEST):
        for field in self.getSearchSchema().getFields():
            fieldName = field.getName()
            self.shownFields[fieldName] = REQUEST.get('show_'+fieldName, False)

    def storeShownResult(self, REQUEST):
        for field in self.getResultsSchema().getFields():
            fieldName = field.getName()
            self.shownResultsFields[fieldName] = REQUEST.get(
                                            'show_result_'+fieldName, False)

    def getCatalogSearchArguments(self, REQUEST):
        searchArguments = {}
        for field in self.getSearchSchema().getFields():
            queryPart = zapi.getMultiAdapter((field, self), IQueryPart)
            value = queryPart.getIndexValue(REQUEST)
            if value is None:
                value = ''
            searchArguments[queryPart.getIndexId()] = value
        return searchArguments

    def to_xml(self, context):
        """Render object to XML.
        """
        f = context.f
        f.write('<silva_find id="%s">' % self.id)
        f.write('</silva_find>')
        
         
                         

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

