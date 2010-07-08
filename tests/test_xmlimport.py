# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from zope.interface.verify import verifyObject

from Products.SilvaFind.interfaces import IFind
from Products.Silva.tests.test_xmlimport import SilvaXMLTestCase

from silva.core.interfaces.events import IContentImported


class XMLImportTestCase(SilvaXMLTestCase):
    """Test import of Silva Find.
    """

    def test_default_find(self):
        """Import a default Silva Find object, With no special data in it.
        """
        self.import_file('test_import_find.silvaxml', globals())

        self.assertEventsAre(
            ['ContentImported for /root/search',],
            IContentImported)

        search = self.root.search
        binding = self.metadata.getMetadata(search)

        self.failUnless(verifyObject(IFind, search))
        self.assertEqual(
            search.get_title(),
            u'Find something in your Site')
        self.assertEqual(
            binding.get('silva-extra', 'content_description'),
            u'This content will find you, even if you hide, it will find you.')
        self.assertEqual(
            binding.get('silva-content', 'maintitle'),
            u'Find something in your Site')
        self.assertEqual(binding.get('silva-extra', 'creator'), u'author')
        self.assertEqual(binding.get('silva-extra', 'lastauthor'), u'paul')

        # Actually those are the fields by default ...
        self.assertListEqual(
            search.shownFields,
            ['fulltext'])
        self.assertListEqual(
            search.shownResultsFields,
            ['breadcrumbs', 'date', 'icon', 'link', 'ranking',
             'resultcount', 'textsnippet', 'thumbnail'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XMLImportTestCase))
    return suite
