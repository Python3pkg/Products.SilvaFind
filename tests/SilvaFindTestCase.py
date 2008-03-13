import os
from Products.Silva.tests import SilvaTestCase
from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Testing import ZopeTestCase
ZopeTestCase.installProduct('SilvaFind')


class SilvaFindTestCase(SilvaTestCase.SilvaTestCase):
    def add_query(self, object, id, title):
        return self.addObject(object, 'SilvaFind', id, title=title,
                              product='SilvaFind')

    
    
    
