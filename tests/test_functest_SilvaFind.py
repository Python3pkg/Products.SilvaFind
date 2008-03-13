import unittest

from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Products.Silva.tests.SilvaBrowser import SilvaBrowser
from Products.Silva.tests.SilvaTestCase import SilvaFunctionalTestCase

class SilvaFindTestCase(SilvaFunctionalTestCase):
    def test_silvafind(self):
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaFindTestCase))
    return suite
