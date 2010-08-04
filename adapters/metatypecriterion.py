# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from five import grok
from megrok.chameleon.components import ChameleonPageTemplate

from Products.Silva.ExtensionRegistry import extensionRegistry
from Products.SilvaFind.adapters.criterion import CriterionTemplateView
from Products.SilvaFind.adapters.criterion import convertValue
from Products.SilvaFind.interfaces import IMetatypeCriterionField, IQuery


class MetatypeCriterionView(CriterionTemplateView):
    grok.adapts(IMetatypeCriterionField, IQuery, Interface)

    template = ChameleonPageTemplate(filename='templates/metatypecriterion.cpt')

    def updateWidget(self, value):
        self.selected = value
        self.types = self.getAvailableMetaTypes()

    def extractWidgetValue(self):
        return convertValue(self.request.get(self.name, None))

    def getAvailableMetaTypes(self):
        meta_types = []
        for content in extensionRegistry.get_addables():
            meta_types.append({"title": content['name'].replace('Silva ', ''),
                               "value": content['name']})
        return meta_types



