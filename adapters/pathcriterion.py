# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.component import getUtility
from zope.traversing.browser import absoluteURL

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from App.class_init import InitializeClass

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaFind.adapters.criterion import (
    StoreCriterion, IndexedCriterion)
from Products.SilvaFind.i18n import translate as _
from Products.Silva.icon import get_icon_url
from silva.core.references.interfaces import IReferenceService
from silva.core.references.reference import get_content_id


EDIT_TEMPLATE = \
r"""
<div id="%(widget_id)s" class="reference-widget">
  <button class="reference-dialog-trigger">
  </button>
  <div id="%(widget_id)s-dialog"
       title="target"
       class="ui-widget reference-dialog">
  </div>
  <a target="_blank" id="%(widget_id)s-link" href="%(target_url)s">
    <img src="%(icon_url)s" />
    %(target_title)s
  </a>
  <input type="hidden"
         name="%(name)s"
         id="%(widget_id)s-value" value="%(value)s">
  <input type="hidden"
         id="%(widget_id)s-interface"
         value="%(interfaces)s">
  <input type="hidden"
         id="%(widget_id)s-base"
         value="%(url)s">
</div>
"""


class StorePathCriterion(StoreCriterion):

    def store(self, request):
        #XXX some room for refactoring here
        field_name = unicode(self.criterion.getName())
        criterion_value = request.get(field_name, None)
        try:
            target_id = int(criterion_value)
        except (ValueError, TypeError,):
            target_id = 0
        reference_service = getUtility(IReferenceService)
        ref = reference_service.get_reference(self.query,
                                              name=field_name,
                                              add=True)
        if ref.target_id != target_id:
            ref.set_target_id(target_id)


class PathCriterionView(Implicit):

    security = ClassSecurityInfo()

    def __init__(self, criterion, query, request):
        self.criterion = criterion
        self.query = query
        self.request = request

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'canBeShown')
    def canBeShown(self):
        return False

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderEditWidget')
    def renderEditWidget(self):
        return self.renderWidget(self.getStoredValue())

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        raise ValueError(u"Cannot render path widgets for the public")

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        name = self.criterion.getName()
        if value is None:
            title = _(u'not set')
            url = '#'
            icon = ''
            content_value = ''
        else:
            title = value.get_title_or_id()
            url = absoluteURL(value, self.request)
            icon = get_icon_url(value, self.request)
            content_value = get_content_id(value)
        return EDIT_TEMPLATE % {
            'name': name,
            'widget_id': "field-%s" % name,
            'url': self.query.get_root_url(),
            'interfaces': 'silva.core.interfaces.content.IContainer',
            'target_title': title,
            'target_url': url,
            'icon_url': icon,
            'value': content_value}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        content = self.getStoredValue()
        if content is None:
            return ''
        return "/".join(content.getPhysicalPath())

    getIndexValue = getValue

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        name = unicode(self.criterion.getName())
        service = getUtility(IReferenceService)
        ref = service.get_reference(self.query, name=name)
        if ref is not None:
            return ref.target
        return None

    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return _('below path')

    def getIndexId(self):
        return 'path'

    security.declareProtected(SilvaPermissions.View, 'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View, 'getDescription')
    def getDescription(self):
        return _('Only search below this location (a path from the site root).')

InitializeClass(PathCriterionView)


class IndexedPathCriterion(IndexedCriterion):

    def getIndexId(self):
        return 'path'
