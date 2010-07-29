# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.component import getUtility

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from App.class_init import InitializeClass

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError
from Products.SilvaFind.i18n import translate as _
from silva.core.references.interfaces import IReferenceService
from silva.core.references.reference import get_content_from_id


EDIT_TEMPLATE = \
r"""
<div id="%(widget_id)s" class="reference-widget">
  <button class="reference-dialog-trigger">
  </button>
  <div id="%(widget_id)s-dialog"
       title="target"
       class="ui-widget reference-dialog">
  </div>
  <a target="_blank" id="%(widget_id)s-link">
    %(target_display)s
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
        value = self.getStoredValue() or ''
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        value = self.getValue() or ''
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        if value is None:
            value = ""
        name = self.criterion.getName()
        return EDIT_TEMPLATE % {
            'name': name,
            'widget_id': "field-%s" % name,
            'url': self.query.get_root_url(),
            'interfaces': 'silva.core.interfaces.content.IContainer',
            'target_display': self.getValue(),
            'value': self.getStoredValue()}

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self):
        field_name = self.criterion.getName()
        value = self.request.get(field_name, None)
        if value:
            pass
            # XXX pathindex does not work with unicode, so do not try
        else:
            try:
                value = int(self.getStoredValue())
                if not value:
                    return ''
            except (ValueError, TypeError,):
                return ''
        content = get_content_from_id(value)
        if content:
            return "/".join(content.getPhysicalPath())
        return ''

    getIndexValue = getValue

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        field_name = unicode(self.criterion.getName())
        reference_service = getUtility(IReferenceService)
        ref = reference_service.get_reference(self.query, name=field_name)
        if ref:
            return ref.target_id
        return None

    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return _('below path')

    def getIndexId(self):
        return 'path'

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        return _('Only search below this location (a path from the site root).')

InitializeClass(PathCriterionView)

class IndexedPathCriterion:
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'path'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' %
                                 id)
