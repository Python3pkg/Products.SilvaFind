# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from five import grok
from silva.core import conf as silvaconf

from Products.Silva.silvaxml.xmlimport import NS_URI, SilvaBaseHandler
from Products.SilvaFind.silvaxml import NS_SILVA_FIND

silvaconf.namespace(NS_URI)


class FindHandler(SilvaBaseHandler):
    grok.name('find')

    def startElementNS(self, name, qname, attrs):
        if name == (NS_URI, 'find'):
            uid = self.generateOrReplaceId(attrs[(None, 'id')].encode('utf-8'))
            factory = self.parent().manage_addProduct['SilvaFind']
            factory.manage_addSilvaFind(uid, '')
            self.setResultId(uid)

    def endElementNS(self, name, qname):
        if name == (NS_URI, 'find'):
            self.storeMetadata()
            self.notifyImport()
