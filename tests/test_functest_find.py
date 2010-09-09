# Copyright (c) 2008-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from Products.Silva.converters import PDF_TO_TEXT_AVAILABLE
from Products.Silva.tests.SilvaBrowser import SilvaBrowser
from Products.Silva.tests.helpers import open_test_file
from Products.Silva.testing import FunctionalLayer


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


class CreateSilvaFindTestCase(unittest.TestCase):
    """Test the Silva find creation.
    """
    layer = FunctionalLayer

    def test_create_silvafind(self):
        """Create and configure a silva find object.
        """

        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
        self.assertEquals(status, 200)

        sb.make_content('Silva Find', id='search_test', title='Search test')

        self.assertTrue('search_test' in sb.get_content_ids())
        sb.click_href_labeled('search_test')

        form = sb.browser.get_form('silva_find_edit')
        form.get_control('show_meta_type:bool').checked = True
        form.get_control('show_silva-content-maintitle:bool').checked = True
        form.get_control('show_silva-extra-keywords:bool').checked = True
        form.get_control('silva-extra.keywords:record').value = 'test-keyword'
        form.get_control('silvafind_save').click()
        self.assertEqual(sb.get_status_feedback(), 'Changes saved.')
        form = sb.browser.get_form('silva_find_edit')
        self.assertEquals(
            form.get_control('show_meta_type:bool').checked, True)
        self.assertEquals(
            form.get_control('show_silva-content-maintitle:bool').checked, True)
        self.assertEquals(
            form.get_control('show_silva-extra-keywords:bool').checked, True)
        self.assertEquals(
            form.get_control('silva-extra.keywords:record').value,
            'test-keyword')


class SilvaFindTestCase(unittest.TestCase):
    """Check if machine has pdftotext. If pdftotext is present run all
    tests, if not leave out pdftotext tests. Test search results of
    SilvaFind.
    """
    layer = FunctionalLayer

    def setUp(self):
        self.root = self.layer.get_application()
        self.layer.login('manager')
        self.root.manage_addProduct['SilvaFind'].manage_addSilvaFind(
            'search_test', 'Search Test')

    def createFile(self, sb, doc):
        """Helper to create a Silva File with the given data.
        """
        factory = self.root.manage_addProduct['Silva']
        with open_test_file(doc['file'], globals()) as file:
            factory.manage_addFile(doc['id'], doc['title'], file)

        sb.go(sb.smi_url())
        ids = sb.get_content_ids()
        self.assertTrue(doc['id'] in ids)

    def changeMetadata(self, sb, doc):
        """Edit metadata of an object.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled(doc['id'])
        sb.click_tab_named('properties')
        form = sb.browser.get_form('form')
        form.get_control('silva-extra.keywords:record').value = doc['keywords']
        form.get_control('save_metadata:method').click()
        self.assertEqual(sb.get_status_feedback(), 'Metadata saved.')
        form = sb.browser.get_form('form')
        self.assertEquals(
            form.get_control('silva-extra.keywords:record').value,
            doc['keywords'])

    def configureSearch(self, sb, keyword):
        """Configure search object.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled('search_test')
        form = sb.browser.get_form('silva_find_edit')
        form.get_control('show_meta_type:bool').checked = True
        form.get_control('show_silva-content-maintitle:bool').checked = True
        form.get_control('show_silva-extra-keywords:bool').checked = True
        form.get_control('silva-extra.keywords:record').value = keyword
        form.get_control('silvafind_save').click()
        form = sb.browser.get_form('silva_find_edit')
        self.assertEquals(
            form.get_control('show_meta_type:bool').checked, True)
        self.assertEquals(
            form.get_control('show_silva-content-maintitle:bool').checked, True)
        self.assertEquals(
            form.get_control('show_silva-extra-keywords:bool').checked, True)
        self.assertEquals(
            form.get_control('silva-extra.keywords:record').value, keyword)

    def search(self, sb, doc):
        """Search terms documents.
        """
        sb.go(sb.smi_url())
        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        form = sb.browser.get_form('search_form')
        test_fulltext = (doc['format'] != 'pdf' or PDF_TO_TEXT_AVAILABLE)
        if test_fulltext:
            form.get_control('fulltext').value = doc['fulltext']
        form.get_control('silva-content.maintitle:record').value = doc['title']
        self.assertEqual(200, form.submit(name='search_submit'))
        link = sb.browser.get_link(doc['title'])
        if test_fulltext:
            self.assertTrue(doc['fulltext'] in sb.contents)
        self.assertTrue(link.html.text_content() in sb.contents)

    def test_empty_search(self):
        """Test to search just by clicking on the search button.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
        self.assertEquals(status, 200)

        msg = 'You need to fill at least one field in the search form.'

        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)

        form = sb.browser.get_form('search_form')
        self.assertEqual(200, form.submit(name='search_submit'))
        self.assertTrue(msg in sb.contents)

    def test_noresult_search(self):
        """Try to make a search which match no results at all.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
        self.assertEquals(status, 200)

        msg = 'No items matched your search.'

        sb.click_href_labeled('search_test')
        sb.click_href_labeled('view...')
        self.failIf(msg in sb.contents)

        # I don't think by default you will have document with that
        form = sb.browser.get_form('search_form')
        form.get_control('fulltext').value = 'blablaxyz'
        form.submit('search_submit')
        self.assertTrue(msg in sb.contents)

    def test_search_in_pdf(self):
        """Test search inside a PDF file.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
        self.assertEquals(status, 200)

        pdf = test_fixture['the_great_figure']
        self.createFile(sb, pdf)
        self.configureSearch(sb, '')
        self.search(sb, pdf)

    def test_search(self):
        """Test search with a regular file.
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
        self.assertEquals(status, 200)

        doc = test_fixture['the_raven']
        self.createFile(sb, doc)
        self.configureSearch(sb, '')
        self.search(sb, doc)

    def test_search_keywords(self):
        """Test search using metadata keywords
        """
        sb = SilvaBrowser()
        status, url = sb.login('manager', 'manager', sb.smi_url())
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
