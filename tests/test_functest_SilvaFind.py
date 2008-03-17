import unittest

from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Products.Silva.tests.SilvaBrowser import SilvaBrowser
from Products.Silva.tests.SilvaTestCase import SilvaFunctionalTestCase


        
class SilvaFindTestCase(SilvaFunctionalTestCase):
    """
        check if machine has pdftotext
        if pdftotext is present run all tests, if not leave out pdftotext tests.
        test search results of SilvaFind
    """
    def content(self, sb, pdf=True):
        sb.make_content('Silva Find', id='search_test',
                                      title='Search test')
        ids = sb.get_content_ids()
        self.failUnless('search_test' in ids)
        if pdf:
            sb.make_content('Silva File', id='the_raven',
                                      title='The Raven',
                                      file='raven.txt')
            sb.make_content('Silva File', id='second_coming',
                                      title='The Second Coming',
                                      file='the_second_coming.txt')
            sb.make_content('Silva File', id='great_figure',
                                          title='The Great Figure',
                                          file='the_great_figure.pdf')
            ids = sb.get_content_ids()
            self.failUnless('the_raven' in ids)
            self.failUnless('second_coming' in ids)
            self.failUnless('great_figure' in ids)
        else:
            sb.make_content('Silva File', id='the_raven',
                                      title='The Raven',
                                      file='raven.txt')
            sb.make_content('Silva File', id='second_coming',
                                      title='The Second Coming',
                                      file='the_second_coming.txt')
            ids = sb.get_content_ids()
            self.failUnless('the_raven' in ids)
            self.failUnless('second_coming' in ids)
        
    def searching(self, sb, pdf=True):
        if pdf:
            
        pass
        
    
    def test_silvafind(self):
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)
        if PDF_TO_TEXT_AVAILABLE:
            # run SilvaFind with pdf tests
            self.content(sb)
        else:
            # run SilvaFind with no pdf tests
            print """
                  pdftotext is not installed.
                  SilvaFind test will continue without testing pdf find functionality!
                  Please install pdftotext and restart the test to fully test SilvaFind
                  """
            self.content(sb, pdf=None)
        sb.click_href_labeled('Search test')
        self.failUnless('edit' in sb.browser.contents)
        self.searching(sb)
        status, url =sb.click_href_labeled('logout')
        self.assertEquals(status, 401)
        

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaFindTestCase))
    return suite
