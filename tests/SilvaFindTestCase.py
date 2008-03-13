from Products.Silva.tests import SilvaTestCase

from Testing import ZopeTestCase
ZopeTestCase.installProduct('SilvaFind')

class SilvaFindTestCase(SilvaTestCase.SilvaTestCase):
    def add_query(self, object, id, title):
        return self.addObject(object, 'SilvaFind', id, title=title,
                              product='SilvaFind')
    
