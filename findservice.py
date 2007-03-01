# Copyright (c) 2002-2006 Infrae. All rights reserved.
# See also LICENSE.txt
# Python

# Zope
from OFS import Folder
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# Silva
from Products.Silva import helpers
from Products.SilvaFind.globalschema import globalSearchFields, globalResultsFields

from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema
from Products.SilvaFind.schema import MetadataResultField
from Products.SilvaFind.schema import MetadataCriterionField
from Products.SilvaFind.schema import DateRangeMetadataCriterionField
from Products.SilvaFind.schema import IntegerRangeMetadataCriterionField

class FindService(Folder.Folder):
    """Find Service
    """
    
    security = ClassSecurityInfo()

    meta_type = "Silva Find Service"
    
    manage_options = (
        () +
        Folder.Folder.manage_options
        )
    #needed to be able to add a SilvaFind object
    def __init__(self, id):
        FindService.inheritedAttribute('__init__')(self, id)
        self.search_schema = None
        self.result_schema = None
    
    def _add_ordered_id(self, item):
        pass

    def _remove_ordered_id(self, item):
        pass

    def getSearchSchema(self):
        if not self.search_schema is None:
            return self.search_schema
        metadata_fields = self._createMetadataCriterionFields()
        return SearchSchema(globalSearchFields + metadata_fields)

    def getResultsSchema(self):
        if not self.result_schema is None:
            return self.result_schema
        metadata_fields = self._createMetadataResultFields()
        fields = globalResultsFields[:-3] + metadata_fields + globalResultsFields[-3:]
        return ResultsSchema(fields)

    def _createMetadataResultFields(self):
        fields = []
        service = self.get_root().service_metadata
        for set in service.getCollection().getMetadataSets():
            for el in set.getElements():
                if el.id == 'hide_from_tocs':
                    continue
                id = '%s:%s' % (set.id, el.id)
                title = el.Title()
                field = MetadataResultField(id, title)
                field.description = el.Description()
                field.setMetadataElement(el)
                fields.append(field)
        return fields

    def _createMetadataCriterionFields(self):
        fields = []
        service = self.get_root().service_metadata
        for set in service.getCollection().getMetadataSets():
            for el in set.getElements():
                if not el.index_p:
                    continue
                id = '%s:%s' % (set.id, el.id)
                if el.index_type == 'DateIndex':
                    field = DateRangeMetadataCriterionField(set.id, el.id)
                else:
                    field = MetadataCriterionField(set.id, el.id)
                fields.append(field)
        return fields
InitializeClass(FindService)

def manage_addFindService(
    context, id='service_find', title='', REQUEST=None):
    """Add find service.
    """    
    service = FindService(id)
    service.title = 'Find Service'
    context._setObject(id, service)
    service = getattr(context, id)
    helpers.add_and_edit(context, id, REQUEST)
    return ''
