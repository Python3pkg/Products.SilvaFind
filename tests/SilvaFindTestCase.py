from Products.Silva.tests import SilvaTestCase

from Testing import ZopeTestCase
ZopeTestCase.installProduct('SilvaFind')


class SilvaFindTestCase(SilvaTestCase.SilvaTestCase):
    def add_query(self, object, id, title):
        return self.addObject(object, 'SilvaFind', id, title=title,
                              product='SilvaFind')
    
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager, getSecurityManager
import time
import transaction

def installSilvaFindExtension(app, quiet=0):
    '''Installs SilvaFind extension.'''
    _start = time.time()
    if not quiet:
        ZopeTestCase._print('Installing SilvaFind extension... ')
    ext = app.root.service_extensions
    if not ext.is_installed('SilvaFind'):
        ext.install('SilvaFind')
    noSecurityManager()
    transaction.commit()
    if not quiet:
        ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

installSilvaFindExtension(ZopeTestCase.app())
