# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import operator

# Zope
from AccessControl import ClassSecurityInfo, getSecurityManager
from App.class_init import InitializeClass
from OFS.SimpleItem import SimpleItem
from Products.ZCTextIndex.ParseTree import ParseError
from ZODB.PersistentMapping import PersistentMapping

# Zope 3
from five import grok
from zope.component import getMultiAdapter
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from zope import component

# Silva
from Products.Silva.Content import Content
from Products.SilvaFind.i18n import translate as _
from Products.Silva import SilvaPermissions

from silva.core import conf as silvaconf
from silva.core.views import views as silvaviews
from silva.core.smi import smi as silvasmi
from zeam.form import silva as silvaforms
from zeam.utils.batch import batch
from zeam.utils.batch.interfaces import IBatching

# SilvaFind
from Products.SilvaFind.query import Query
from Products.SilvaFind.interfaces import IFind
from Products.SilvaFind.adapters.interfaces import ICriterionView
from Products.SilvaFind.interfaces import IResultView
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
    silvaconf.icon('SilvaFind.png')

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

    security.declareProtected(SilvaPermissions.View, 'getPublicResultFields')
    def getPublicResultFields(self):
        return filter(lambda field: self.isResultShown(field.getName()),
                      self.getResultFields())

    security.declareProtected(SilvaPermissions.View, 'getPublicSearchFields')
    def getPublicSearchFields(self):
        return filter(lambda field: self.isCriterionShown(field.getName()),
                      self.getSearchFields())

    security.declareProtected(SilvaPermissions.View, 'isCriterionShown')
    def isCriterionShown(self, fieldName):
        return self.shownFields.get(fieldName, False)

    security.declareProtected(SilvaPermissions.View, 'isResultShown')
    def isResultShown(self, fieldName):
        return self.shownResultsFields.get(fieldName, False)

    security.declareProtected(SilvaPermissions.View, 'isFormNeeded')
    def isFormNeeded(self):
        return reduce(operator.or_, self.shownFields.values())

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
            return ([], _(
                    u'Search query can not start with wildcard character.'))
        if queryEmpty:
            return ([], _(
                    u'You need to fill at least one field in the search form.'))
        try:
            results = catalog.searchResults(searchArguments)
        except ParseError:
            return ([], _(
                    u'Search query contains only common or reserved words.'))

        if not results:
            return ([], _(u'No items matched your search.'))

        return (results, '')

    def _edit(self, request):
        """Store fields values
        """
        # Validate values
        def validate(prefix, schema):
            atLeastOneShown = False
            for field in schema.getFields():
                shown = request.get(prefix + field.getName(), False)
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
        for field in self.getSearchFields():
            storeCriterion = getMultiAdapter((field, self), IStoreCriterion)
            storeCriterion.store(request)

    def storeShownCriterion(self, request):
        for field in self.getSearchFields():
            fieldName = field.getName()
            self.shownFields[fieldName] = bool(
                request.form.get('show_' + fieldName, False))

    def storeShownResult(self, request):
        for field in self.getResultFields():
            fieldName = field.getName()
            self.shownResultsFields[fieldName] = bool(
                request.form.get('show_result_' + fieldName, False))

    def getCatalogSearchArguments(self, request):
        searchArguments = {}
        for field in self.getSearchFields():
            name = field.getName()
            if (self.shownFields.get(name, False) or name == 'path'):
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


class SilvaFindEditView(silvasmi.SMIPage):
    """Edit a Silva Find
    """
    grok.context(IFind)
    grok.name('tab_edit')
    grok.require('silva.ChangeSilvaContent')

    tab = 'edit'

    def update(self):
        self.search_widgets = []
        for field in self.context.getSearchFields():
            widget = getMultiAdapter((
                    field, self.context, self.request), ICriterionView)
            self.search_widgets.append(widget)

        self.title = self.context.get_title_or_id()

        if 'silvafind_save' in self.request.form:
            message, message_type = self.context._edit(self.request)
            self.send_message(message, message_type)


class SilvaFindView(silvaviews.View):
    """View a Silva Find.
    """
    grok.context(IFind)

    def update(self):
        # Do search
        checkPermission = getSecurityManager().checkPermission
        results, self.message = \
            self.context.searchResultsWithDescription(self.request)
        # Filter results on View permission
        # XXX This could be done more in a more lazy fashion
        results = filter(
            lambda b: checkPermission('View', b.getObject()),
            results)
        self.results = batch(results, count=20, request=self.request)
        self.result_widgets = []
        self.batch = u''
        if self.results:
            for result in self.context.getPublicResultFields():
                widget = getMultiAdapter((
                        self.context, result, self.request), IResultView)
                widget.update(self.results)
                self.result_widgets.append(widget)

            self.batch = component.getMultiAdapter(
                (self.context, self.results, self.request), IBatching)()

        # Search Widgets
        self.search_widgets = []
        for field in self.context.getPublicSearchFields():
            widget = getMultiAdapter((
                    field, self.context, self.request), ICriterionView)
            self.search_widgets.append(widget)


