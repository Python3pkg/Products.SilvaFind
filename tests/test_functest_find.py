# Copyright (c) 2008-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import os
import unittest
from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Products.Silva.tests.SilvaBrowser import SilvaBrowser, SILVA_FORM, \
    Z3CFORM_FORM
from Products.Silva.tests.SilvaTestCase import SilvaFunctionalTestCase

test_fixture = {
    'the_great_figure': {
        'id': 'the_great_figure.pdf',
        'title': 'The Great Figure',
        'file': 'the_great_figure.pdf',
        'fulltext': 'gold',
        'short_title': '',
        'keywords': '',
        'format': 'pdf',
    },
    'the_raven': {
        'id': 'the_raven.txt',
        'title': 'The Raven',
        'file': 'raven.txt',
        'fulltext': 'bleak',
        'short_title': '',
        'keywords': '',
        'format': 'txt',
    },
    'the_second_coming': {
        'id': 'the_second_coming.txt',
        'title': 'The Second Coming',
        'file': 'the_second_coming.txt',
        'fulltext': 'Spiritus Mundi',
        'short_title': '',
        'keywords': 'yeats',
        'format': 'txt',
    },
}


class CreateSilvaFindTestCase(SilvaFunctionalTestCase):
    """Test the Silva find creation.
    """

    def test_create_silvafind(self):
        """Create and configure a silva find object.
        """

        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        sb.make_content('Silva Find', id='search_test', title='Search test')

        ids = sb.get_content_ids()
        self.failUnless('search_test' in ids)
        sb.click_href_labeled('search_test')

        browser = sb.browser
        form = sb.browser.getForm(index=0)
        form.getControl(
            name='show_meta_type:bool').value = ['checked']
        form.getControl(
            name='show_silva-content-maintitle:bool').value = ['checked']
        form.getControl(
            name='show_silva-extra-keywords:bool').value = ['checked']
        form.getControl(
            name='silva-extra.keywords:record').value = 'test-keyword'
        form.submit()
        form = sb.browser.getForm(index=0)
        self.failUnless('Changes saved.' in sb.browser.contents)
        self.assertEquals(
            form.getControl(name='show_meta_type:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='show_silva-content-maintitle:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='show_silva-extra-keywords:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='silva-extra.keywords:record').value,
            'test-keyword')



class SilvaFindTestCase(SilvaFunctionalTestCase):
    """Check if machine has pdftotext. If pdftotext is present run all
    tests, if not leave out pdftotext tests. Test search results of
    SilvaFind.
    """

    def afterSetUp(self):
        self.root.manage_addProduct['SilvaFind'].manage_addSilvaFind(
            'search_test', 'Search Test')

    def createFile(self, sb, doc):
        """Helper to create a Silva File with the given data.
        """
        directory = os.path.dirname(__file__)
        file_handle = open(os.path.join(directory, 'data', doc['file']))
        self.root.manage_addProduct['Silva'].manage_addFile(
            doc['id'], doc['title'], file_handle)
        file_handle.close()

        sb.go(sb.smi_url())
        ids = sb.get_content_ids()
        self.failUnless(doc['id'] in ids)

    def changeMetadata(self, sb, doc):
        """Edit metadata of an object.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled(doc['id'])
        sb.click_tab_named('properties')
        sb.browser.getControl(
            name='silva-extra.keywords:record').value = doc['keywords']
        sb.browser.getControl(name='save_metadata:method', index=0).click()
        feedback = sb.get_status_feedback()
        self.failUnless(
            feedback.startswith('Metadata saved.'))
        self.assertEquals(
            sb.browser.getControl(name='silva-extra.keywords:record').value,
            doc['keywords'])

    def configureSearch(self, sb, keyword):
        """Configure search object.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled('search_test')
        form = sb.browser.getForm(index=0)
        form.getControl(
            name='show_meta_type:bool').value = ['checked']
        form.getControl(
            name='show_silva-content-maintitle:bool').value = ['checked']
        form.getControl(
            name='show_silva-extra-keywords:bool').value = ['checked']
        form.getControl(
            name='silva-extra.keywords:record').value = keyword
        form.submit()
        form = sb.browser.getForm(index=0)
        self.assertEquals(
            form.getControl(name='show_meta_type:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='show_silva-content-maintitle:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='show_silva-extra-keywords:bool').value,
            True)
        self.assertEquals(
            form.getControl(name='silva-extra.keywords:record').value,
            keyword)

    def search(self, sb, doc):
        """Search terms documents.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        test_fulltext = (doc['format'] != 'pdf' or PDF_TO_TEXT_AVAILABLE)
        if test_fulltext:
            sb.browser.getControl(name='fulltext').value = doc['fulltext']
        sb.browser.getControl(
            name='silva-content.maintitle:record').value = doc['title']
        sb.click_button_labeled('Search')
        link = sb.browser.getLink(doc['title'])
        if test_fulltext:
            self.failUnless(doc['fulltext'] in sb.contents)
        self.failUnless(link.text in sb.contents)

    def test_empty_search(self):
        """Test to search just by clicking on the search button.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        msg = 'You need to fill at least one field in the search form.'

        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)

        sb.click_button_labeled('Search')
        self.failUnless(msg in sb.contents)

    def test_noresult_search(self):
        """Try to make a search which match no results at all.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        msg = 'No items matched your search.'

        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)

        # I don't think by default you will have document with that
        sb.browser.getControl(name='fulltext').value = 'blablaxyz'
        sb.click_button_labeled('Search')
        self.failUnless(msg in sb.contents)

    def test_search_in_pdf(self):
        """Test search inside a PDF file.
        """

        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        pdf = test_fixture['the_great_figure']
        self.createFile(sb, pdf)
        self.configureSearch(sb, '')
        self.search(sb, pdf)

    def test_search(self):
        """Test search with a regular file.
        """

        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        doc = test_fixture['the_raven']
        self.createFile(sb, doc)
        self.configureSearch(sb, '')
        self.search(sb, doc)

    def test_search_keywords(self):
        """Test search using metadata keywords
        """

        sb = SilvaBrowser()
        status, url = sb.login('manager', 'secret', sb.smi_url())
        self.assertEquals(status, 200)

        doc = test_fixture['the_second_coming']
        self.createFile(sb, doc)
        self.changeMetadata(sb, doc)
        self.configureSearch(sb, doc['keywords'])
        self.search(sb, doc)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CreateSilvaFindTestCase))
    suite.addTest(unittest.makeSuite(SilvaFindTestCase))
    return suite
