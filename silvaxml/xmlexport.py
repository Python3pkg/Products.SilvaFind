# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from five import grok

from Products.SilvaFind import interfaces
from Products.SilvaFind.silvaxml import NS_SILVA_FIND
from Products.Silva.silvaxml.xmlexport import SilvaBaseProducer, theXMLExporter

theXMLExporter.registerNamespace('silva-find', NS_SILVA_FIND)


class FindProducer(SilvaBaseProducer):
    """XML export a Silva Find object.
    """
    grok.adapts(interfaces.IFind, Interface)

    def sax(self):

        def serializeOptions(name, options):
            self.startElementNS(NS_SILVA_FIND, name)
            for field_id, activated in options.items():
                if activated:
                    self.startElementNS(
                        NS_SILVA_FIND, 'field', {'name': field_id})
                    self.endElementNS(
                        NS_SILVA_FIND, 'field')
            self.endElementNS(NS_SILVA_FIND, name)

        self.startElement('find', {'id': self.context.id})
        self.metadata()
        serializeOptions('search', self.context.shownFields)
        serializeOptions('display', self.context.shownResultsFields)
        self.startElementNS(NS_SILVA_FIND, 'default')
        self.endElementNS(NS_SILVA_FIND, 'default')
        self.endElement('find')
