# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Silva
from Products.SilvaFind.adapters.criterion import StoreCriterion, CriterionView


class StoreFullTextCriterion(StoreCriterion):

    def store(self, request):
        field_name = self.criterion.getName()
        criterion_value = unicode(request.get(field_name, None),'UTF-8')
        if criterion_value is None:
            return
        self.query.setCriterionValue(field_name, criterion_value)


class FullTextCriterionView(CriterionView):


    def canBeShown(self):
        return True

    def renderEditWidget(self):
        value = self.getStoredValue()
        return self.renderWidget(value)

    def renderPublicWidget(self):
        value = self.getValue()
        return {'name': self.criterion.getName(),
                'field_type': self.__class__.__name__,
                'value': value,}

    def renderWidget(self, value):
        if value is None:
            value = ""
        html = '''
        <input class="store" type="text" name="%s" id="%s" value="%s" size="20" />
        '''
        return html % (self.criterion.getName(),
                       self.criterion.getName(),
                       value)

    def getValue(self):
        field_name = self.criterion.getName()
        value = self.request.get(field_name, None)
        if value:
            value = unicode(value, 'UTF-8')
        else:
            value = self.getStoredValue()
        return value

    getIndexValue = getValue

    def getStoredValue(self):
        value = self.query.getCriterionValue(self.criterion.getName())
        return value


