"""Install for Silva Find
"""

# zope3
from zope.app import zapi

# Silva
from Products.Silva.install import add_fss_directory_view

# SilvaFind
from Products.SilvaFind import SilvaFind
from Products.SilvaFind import globalSearchSchema
from Products.SilvaFind.interfaces import IIndexedField

def install(root):
    # create the core views from filesystem
    add_fss_directory_view(root.service_views,
                           'SilvaFind', __file__, 'views')
    # also register views
    registerViews(root.service_view_registry)

    # security
    root.manage_permission('Add Silva Finds',
                           ['Editor', 'ChiefEditor', 'Manager'])

    root.service_metadata.addTypesMapping(('Silva Find', ), ('silva-content', 'silva-extra'))

    checkIndexes(root)

def uninstall(root):
    unregisterViews(root.service_view_registry)
    root.service_views.manage_delObjects(['SilvaFind'])
    
def is_installed(root):
    return hasattr(root.service_views, 'SilvaFind')

def registerViews(reg):
    """Register core views on registry.
    """
    # edit
    reg.register('edit', 'Silva Find', ['edit', 'Content', 'SilvaFind'])
    # public
    reg.register('public', 'Silva Find', ['public', 'SilvaFind', 'view'])
    # add
    reg.register('add', 'Silva Find', ['add', 'SilvaFind'])
    # preview
    reg.register('preview', 'Silva Find', ['public', 'SilvaFind', 'preview'])
    
def unregisterViews(reg):
    for meta_type in ['Silva Find']:
        reg.unregister('edit', meta_type)
        reg.unregister('add', meta_type)
        reg.unregister('preview', '%s Version' % meta_type)

def checkIndexes(root):
    """check that all searchSchema fields are indexed
    """

    for field in globalSearchSchema.getFields():
        indexedField = zapi.getMultiAdapter((field, root), IIndexedField)
        indexedField.checkIndex()

