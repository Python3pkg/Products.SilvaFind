# Copyright (c) 2002-2006 Infrae. All rights reserved.
# See also LICENSE.txt
# Python

# Zope
from OFS import Folder
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# Silva
from Products.Silva import helpers
from Products.SilvaFind.globalschema import globalSearchSchema, globalResultsSchema 

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
        self.search_schema = globalSearchSchema
        self.results_schema = globalResultsSchema
    
    def _add_ordered_id(self, item):
        pass

    def getSearchSchema(self):
        return self.search_schema

    def getResultsSchema(self):
        return self.results_schema
    
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