# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from zope.interface import Interface

from Products.SilvaFind.adapters.criterion import CriterionView
from Products.SilvaFind.interfaces import IQuery, IFullTextCriterionField


HTML = u"""<input class="store" type="text"
                  name="%s" id="%s" value="%s" size="20" />"""


class FullTextCriterionView(CriterionView):
    grok.adapts(IFullTextCriterionField, IQuery, Interface)

    def renderWidget(self, value):
        if value is None:
            value = ""
        return HTML % (self.name, self.name, value)

    def extractWidgetValue(self):
        value = self.request.get(self.name, None)
        if value is None:
            return None
        return unicode(value, 'UTF-8')

