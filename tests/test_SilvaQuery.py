# Copyright (c) 2006-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Zope 3
from zope.interface.verify import verifyObject

from Products.Silva.tests.SilvaTestCase import SilvaTestCase
from Products.Silva.tests.helpers import publishObject
from Products.SilvaFind.interfaces import IFind


class SilvaQueryTestCase(SilvaTestCase):
    """Test some silva find features.
    """

    def afterSetUp(self):
        self.add_find(self.root, 'query', 'Query')

    def test_find(self):
        self.failUnless('query' in self.root.objectIds())
        verifyObject(IFind, self.root.query)


import unittest
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SilvaQueryTestCase))
    return suite
