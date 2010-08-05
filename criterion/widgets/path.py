# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from megrok.chameleon.components import ChameleonPageTemplate
from zope.component import getUtility
from zope.interface import Interface
from zope.traversing.browser import absoluteURL

from Products.Silva.icon import get_icon_url
from Products.SilvaFind.criterion.widgets.default import CriterionData
from Products.SilvaFind.criterion.widgets.default import CriterionTemplateView
from Products.SilvaFind.i18n import translate as _
from Products.SilvaFind.interfaces import IPathCriterionField, IQuery

from silva.core.references.interfaces import IReferenceService
from silva.core.references.reference import get_content_id


class PathCriterionData(CriterionData):
    grok.adapts(IPathCriterionField, IQuery)

    def __init__(self, criterion, query):
        super(PathCriterionData, self).__init__(criterion, query)
        self.service = getUtility(IReferenceService)

    def getValue(self):
        reference = self.service.get_reference(self.query, name=self.name)
        if reference is not None:
            return reference.target
        return None

    def setValue(self, value):
        assert isinstance(value, int)
        reference = self.service.get_reference(
            self.query, name=self.name, add=True)
        if reference.target_id != value:
            reference.set_target_id(value)


class PathCriterionView(CriterionTemplateView):
    grok.adapts(IPathCriterionField, IQuery, Interface)

    template = ChameleonPageTemplate(filename="templates/pathcriterion.cpt")
    interface = 'silva.core.interfaces.content.IContainer'

    def renderPublicWidget(self):
        raise ValueError(u"Cannot render path widgets for the public")

    def updateWidget(self, value):
        self.title = _(u'not set')
        self.url = '#'
        self.icon = ''
        self.value = ''
        if value is not None:
            self.title = value.get_title_or_id()
            self.url = absoluteURL(value, self.request)
            self.icon = get_icon_url(value, self.request)
            self.value = get_content_id(value)

    def extractWidgetValue(self):
        value = self.request.get(self.name, None)
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def getIndexValue(self):
        content = self.data.getValue()
        if content is None:
            return ''
        return "/".join(content.getPhysicalPath())




