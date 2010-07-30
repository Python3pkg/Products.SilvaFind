# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from zope import component
from five import grok

from Products.SilvaFind import interfaces
from Products.SilvaFind.silvaxml import NS_SILVA_FIND
from Products.SilvaFind.adapters.interfaces import ICriterionView
from Products.Silva.silvaxml.xmlexport import SilvaBaseProducer, theXMLExporter

theXMLExporter.registerNamespace('silva-find', NS_SILVA_FIND)


class FindProducer(SilvaBaseProducer):
    """XML export a Silva Find object.
    """
    grok.adapts(interfaces.IFind, Interface)

    def sax(self):

        schema = self.context.getSearchSchema()
        request = self.getSettings().request

        def searchValues(field_id):
            field = schema.getField(field_id)
            view = component.getMultiAdapter(
                (field, self.context, request), ICriterionView)
            view.serializeXML(self, self.context.searchValues.get(field_id))

        def serializeOptions(name, options, handler=None):
            self.startElementNS(NS_SILVA_FIND, name)
            for field_id, activated in options.items():
                if activated:
                    self.startElementNS(
                        NS_SILVA_FIND, 'field', {'name': field_id})
                    if handler is not None:
                        handler(field_id)
                    self.endElementNS(
                        NS_SILVA_FIND, 'field')
            self.endElementNS(NS_SILVA_FIND, name)

        self.startElement('find', {'id': self.context.id})
        self.metadata()
        serializeOptions('search', self.context.shownFields, searchValues)
        serializeOptions('display', self.context.shownResultsFields)
        self.startElementNS(NS_SILVA_FIND, 'default')
        self.endElementNS(NS_SILVA_FIND, 'default')
        self.endElement('find')
