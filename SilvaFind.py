# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Zope
from AccessControl import ClassSecurityInfo, getSecurityManager
from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.ZCTextIndex.ParseTree import ParseError
from ZODB.PersistentMapping import PersistentMapping

# Zope 3
from five import grok
from zope.component import getMultiAdapter, getUtility
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from zope import component

# Silva
from Products.Silva.Content import Content
from Products.SilvaFind.i18n import translate as _
from Products.Silva import SilvaPermissions

from silva.core import conf as silvaconf
from silva.core.views import views as silvaviews
from zeam.form import silva as silvaforms
from zeam.utils.batch import batch
from zeam.utils.batch.interfaces import IBatching

# SilvaFind
from Products.SilvaFind.query import Query
from Products.SilvaFind.interfaces import IFind, IFindService
from Products.SilvaFind.adapters.interfaces import ICriterionView
from Products.SilvaFind.adapters.interfaces import IResultView
from Products.SilvaFind.adapters.interfaces import IQueryPart
from Products.SilvaFind.adapters.interfaces import IStoreCriterion


class SilvaFind(Query, Content, SimpleItem):
    __doc__ = _("""Silva Find is a powerful search feature that allows easy
        creation of search forms and result pages. Users can add a Find
        anywhere and define which fields to make searchable by site visitors
        and/or which fields to limit to a preset value. Users also can
        determine which fields should be displayed in the search results. All
        metadata sets/fields are supported.""")

    security = ClassSecurityInfo()

    meta_type = "Silva Find"
    grok.implements(IFind)
    silvaconf.icon('find.png')

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

    security.declareProtected(SilvaPermissions.View, 'getFieldViews')
    def getFieldViews(self, request):
        result = []
        for field in self.getSearchSchema().getFields():
            searchFieldView = getMultiAdapter((field, self, request),
                ICriterionView)
            # wrapped to enable security checks
            searchFieldView = searchFieldView.__of__(self)
            result.append(searchFieldView)
        return result

    security.declareProtected(SilvaPermissions.View, 'getPublicFieldViews')
    def getPublicFieldViews(self, request):
        return filter(
            lambda view: self.isCriterionShown(view.getName()),
            self.getFieldViews(request))

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

    security.declareProtected(SilvaPermissions.View,
                             'searchResultsWithDescription')
    def searchResultsWithDescription(self, request={}):
        if not request.has_key('search_submit'):
            return ([], '')
        catalog = self.get_root().service_catalog
        searchArguments = self.getCatalogSearchArguments(request)
        queryEmpty = True
        for key, value in searchArguments.items():
            if key in ['path', 'meta_type']:
                # these fields do not count as a real search query
                # they are always there to filter unwanted results
                continue
            if type(value) is unicode and value.strip():
                queryEmpty = False
                break
            elif type(value) is list:
                queryEmpty = False
                break
        searchArguments['version_status'] = ['public']
        query = searchArguments.get('fulltext', '').strip()
        if query and query[0] in ['?', '*']:
            return ([], _('Search query can not start '
                            'with wildcard character.'))
        if queryEmpty:
            return ([], _('You need to fill at least one '
                          'field in the search form.'))
        try:
            results = catalog.searchResults(searchArguments)
        except ParseError:
            return ([], _('Search query contains only common '
                            'or reserved words.'))

        if not results:
            return ([], _('No items matched your search.'))

        return (results, '')

    security.declareProtected(SilvaPermissions.View, 'getResultFieldViews')
    def getResultFieldViews(self):
        result = []
        for field in getUtility(IFindService).getResultsSchema().getFields():
            resultFieldView = getMultiAdapter((field, self), IResultView)
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
        return [(field.getColumnTitle(), field.render)
                for field in self.getResultsSchema().getFields()]

    security.declareProtected(SilvaPermissions.View, 'searchResultsObjects')
    def searchResultsObjects(self, request={}):
        results = self.searchResults(request)
        return [result.getObject().get_silva_object() for result in results]


    #MUTATORS
    security.declareProtected(
        SilvaPermissions.ChangeSilvaContent, 'manage_edit')
    def manage_edit(self, REQUEST):
        """Store fields values
        """
        message, message_type = self._edit(REQUEST)
        return self.edit['tab_edit'](message=message, message_type=message_type)

    def _edit(self, request):
        """Store fields values
        """
        # Validate values
        def validate(name, schema):
            atLeastOneShown = False
            for field in schema.getFields():
                fieldName = field.getName()
                shown = request.get(name + fieldName, False)
                atLeastOneShown = atLeastOneShown or shown
            return atLeastOneShown

        if not validate('show_', self.getSearchSchema()):
            return (_('You need to activate at least one search criterion.'),
                    'error')
        if not validate('show_result_', self.getResultsSchema()):
            return (_('You need to display at least one field in the results.'),
                    'error')
        # Save them
        self.storeCriterionValues(request)
        self.storeShownCriterion(request)
        self.storeShownResult(request)
        notify(ObjectModifiedEvent(self))
        return (_('Changes saved.'), 'feedback')

    #HELPERS
    def storeCriterionValues(self, request):
        for field in self.getSearchSchema().getFields():
            storeCriterion = getMultiAdapter((field, self), IStoreCriterion)
            storeCriterion.store(request)

    def storeShownCriterion(self, request):
        for field in self.getSearchSchema().getFields():
            fieldName = field.getName()
            self.shownFields[fieldName] = bool(
                request.get('show_'+fieldName, False))

    def storeShownResult(self, request):
        for field in self.getResultsSchema().getFields():
            fieldName = field.getName()
            self.shownResultsFields[fieldName] = bool(
                request.get('show_result_'+fieldName, False))

    def getCatalogSearchArguments(self, request):
        searchArguments = {}
        for field in self.getSearchSchema().getFields():
            if (self.shownFields.has_key(field.getName())
                    and self.shownFields.get(field.getName(), False)
                    or field.getName() == 'path'):
                queryPart = getMultiAdapter((field, self, request), IQueryPart)
                value = queryPart.getIndexValue()
                if value is None:
                    value = ''
                searchArguments[queryPart.getIndexId()] = value
        return searchArguments


InitializeClass(SilvaFind)


class SilvaFindAddForm(silvaforms.SMIAddForm):
    """Add form for Silva Find.
    """
    grok.name(u'Silva Find')
    grok.context(IFind)

    description = SilvaFind.__doc__



class SilvaFindView(silvaviews.View):
    """View a Silva Find.
    """
    grok.context(IFind)

    def isViewableForUser(self, brain):
        security_manager = getSecurityManager()
        return security_manager.checkPermission('View', brain.getObject())

    def update(self):
        results, self.message = \
            self.context.searchResultsWithDescription(self.request)
        #self.titles = self.context.getResultsColumnTitles()
        self.results = batch(results, count=20, request=self.request)
        self.fields = self.context.getPublicResultFieldViews()
        self.batch = component.getMultiAdapter(
            (self.context, self.results, self.request), IBatching)()


