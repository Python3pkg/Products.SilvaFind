# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import unittest

from Products.Silva.silvaxml import xmlexport
from Products.Silva.tests.test_xmlexport import SilvaXMLTestCase


class XMLExportTestCase(SilvaXMLTestCase):
    """Test some silva find features.
    """

    def setUp(self):
        super(XMLExportTestCase, self).setUp()
        factory = self.root.manage_addProduct['SilvaFind']
        factory.manage_addSilvaFind('search', 'Search your Site')

    def test_default_export(self):
        """Export a default created Silva Find object.
        """
        xml, info = xmlexport.exportToString(self.root.search)
        self.assertExportEqual(xml, 'test_export_search.silvaxml', globals())
        self.assertEqual(info.getZexpPaths(), [])
        self.assertEqual(info.getAssetPaths(), [])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(XMLExportTestCase))
    return suite
