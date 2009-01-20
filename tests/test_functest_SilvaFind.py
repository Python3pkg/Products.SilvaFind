# Copyright (c) 2008-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import os
import unittest
from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Products.Silva.tests.SilvaBrowser import SilvaBrowser, SILVA_FORM, Z3CFORM_FORM
from Products.Silva.tests.SilvaTestCase import SilvaFunctionalTestCase

content = {
    'the_great_figure': {
        'id': 'the_great_figure',
        'title': 'The Great Figure',
        'file': 'the_great_figure.pdf',
        'fulltext': 'gold',
        'short_title': '',
        'keywords': 'williams',
        'format': 'pdf',
    },
    'the_raven': {
        'id': 'the_raven',
        'title': 'The Raven',
        'file': 'raven.txt',
        'fulltext': 'bleak',
        'short_title': '',
        'keywords': 'poe',
        'format': 'txt',
    },
    'the_second_coming': {
        'id': 'the_second_coming',
        'title': 'The Second Coming',
        'file': 'the_second_coming.txt',
        'fulltext': 'Spiritus Mundi',
        'short_title': '',
        'keywords': 'yeats',
        'format': 'txt',
    },
}


class SilvaFindTestCase(SilvaFunctionalTestCase):
    """
        check if machine has pdftotext
        if pdftotext is present run all tests, if not leave out pdftotext tests.
        test search results of SilvaFind
    """

    def content(self, sb):
        directory = os.path.dirname(__file__)
        for name, doc in content.iteritems():
            file_handle = open(os.path.join(directory, doc['file']))
            file_data = file_handle.read()
            file_handle.seek(0)
            self.root.manage_addProduct['Silva'].manage_addFile(
                doc['id'], doc['title'], file_handle)
            file_handle.close()

        sb.make_content('Silva Find', id='search_test', title='Search test')
        ids = sb.get_content_ids()
        self.failUnless('search_test' in ids)
        self.failUnless('the_raven' in ids)
        self.failUnless('the_second_coming' in ids)
        self.failUnless('the_great_figure' in ids)

        self.modify_text_metadata(sb)

    def modify_text_metadata(self, sb):
        for name, doc in content.iteritems():
            keywords = doc['keywords']
            sb.click_href_labeled(name)
            sb.click_tab_named('properties')
            sb.browser.getControl(name='silva-extra.keywords:record').value = keywords
            sb.browser.getControl(name='save_metadata:method', index=0).click()
            feedback = sb.get_status_feedback()
            self.failUnless(feedback.startswith('Metadata saved.'))
            self.assertEquals(sb.browser.getControl(name='silva-extra.keywords:record').value, keywords)
            sb.click_href_labeled('edit')
            sb.click_href_labeled('root')

    def modify_interface(self, sb, keyword):
        sb.click_href_labeled('search_test')
        form = sb.browser.getForm(index=0)
        form.getControl(name='show_meta_type:bool').value = ['checked']
        form.getControl(name='show_silva-content-maintitle:bool').value = ['checked']
        form.getControl(name='show_silva-extra-keywords:bool').value = ['checked']
        form.getControl(name='silva-extra.keywords:record').value = keyword
        form.submit()
        form = sb.browser.getForm(index=0)
        self.assertEquals(form.getControl(name='show_meta_type:bool').value, True)
        self.assertEquals(form.getControl(name='show_silva-content-maintitle:bool').value, True)
        self.assertEquals(form.getControl(name='show_silva-extra-keywords:bool').value, True)
        self.assertEquals(form.getControl(name='silva-extra.keywords:record').value, keyword)
        sb.go(sb.smi_url())

    def search_empty(self, sb):
        """Just click on search without filling any fields.
        """
        msg = 'You need to fill at least one field in the search form.'
        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)
        sb.click_button_labeled('Search')
        self.failUnless(msg in sb.contents)
        sb.go(sb.smi_url())

    def search_noresult(self, sb):
        """Make a search which gives no results.
        """
        msg = 'No items matched your search.'
        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)
        # I don't think by default you will have document with that
        sb.browser.getControl(name='fulltext').value = 'blablaxyz'
        sb.click_button_labeled('Search')
        self.failUnless(msg in sb.contents)
        sb.go(sb.smi_url())

    def search(self, sb, doc):
        """Search terms documents.
        """
        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        if doc['format'] != 'pdf' or PDF_TO_TEXT_AVAILABLE:
            sb.browser.getControl(name='fulltext').value = doc['fulltext']
        sb.browser.getControl(name='silva-content.maintitle:record').value = doc['title']
        sb.click_button_labeled('Search')
        link = sb.browser.getLink(doc['title'])
        self.failUnless(doc['fulltext'] in sb.contents)
        self.failUnless(link.text in sb.contents)
        sb.go(sb.smi_url())

    def test_search(self):
        """Test silva find objects.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)
        # Setup: Create some contents
        self.content(sb)
        # Test 1 empty search
        self.search_empty(sb)
        # Test 2 invalid search
        self.search_noresult(sb)
        # Test 3 search with docs
        for name, doc in content.iteritems():
            self.modify_interface(sb, doc['keywords'])
            self.search(sb, doc)
        status, url = sb.click_href_labeled('logout')
        self.assertEquals(status, 401)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaFindTestCase))
    return suite
