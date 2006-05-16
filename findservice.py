# Copyright (c) 2002-2006 Infrae. All rights reserved.
# See also LICENSE.txt
# Python

# Zope
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass

# Silva
from Products.Silva import Folder
from Products.Silva import helpers
from Products.Silva import helpers


class FindService(Folder.Folder):
    """Find Service
    """
    
    security = ClassSecurityInfo()

    meta_type = "Silva Find Service"
    
    manage_options = (
        () +
        Folder.Folder.manage_options
        )

        
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
