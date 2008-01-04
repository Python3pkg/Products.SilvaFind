# Copyright (c) 2002-2008 Infrae. All rights reserved.
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
from Products.SilvaFind.schema import AutomaticMetaDataResultField
from Products.SilvaFind.schema import AutomaticMetaDataCriterionField

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
        amd = [obj for obj in globalSearchFields if isinstance(
                obj, AutomaticMetaDataCriterionField)]
        if amd:
            metadata_fields = self._createMetadataCriterionFields()
            amd = amd[0]
            index = globalSearchFields.index(amd)
            fields = (globalSearchFields[:index] 
                        + metadata_fields +
                        globalSearchFields[index:])
            fields.remove(amd)
        else:
            fields = globalSearchFields
        return SearchSchema(fields)

    def getResultsSchema(self):
        if not self.result_schema is None:
            return self.result_schema
        amd = [obj for obj in globalResultsFields if isinstance(
                obj, AutomaticMetaDataResultField)]
        if amd:
            metadata_fields = self._createMetadataResultFields()
            amd = amd[0]
            index = globalResultsFields.index(amd)
            fields = (globalResultsFields[:index] 
                        + metadata_fields +
                        globalResultsFields[index:])
            fields.remove(amd)
        else:
            fields = globalResultsFields
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
                if el.field_type == 'DateTimeField':
                    field = DateRangeMetadataCriterionField(set.id, el.id)
                elif el.field_type == 'IntegerField':
                    field = IntegerRangeMetadataCriterionField(set.id, el.id)
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
