"""Install for Silva Find
"""

# zope3
from zope.component import getUtility

# SilvaFind
from Products.SilvaFind.interfaces import IFindService
from silva.core.services.interfaces import ICatalogService


def install(root):
    # XXX Check CSS resources
    # security
    root.manage_permission('Add Silva Finds',
                           ['Editor', 'ChiefEditor', 'Manager'])

    root.service_metadata.addTypesMapping(
        ('Silva Find', ), ('silva-content', 'silva-extra'))

    setupService(root)
    checkIndexes(root)
    configureAddables(root, ['Silva Find'])


def uninstall(root):
    root.manage_delObjects(['service_find'])


def is_installed(root):
    return hasattr(root, 'service_find')


def configureAddables(root, meta_types):
    addables = root.get_silva_addables_allowed_in_container()
    if addables:
        for meta_type in meta_types:
            if meta_type not in addables:
                addables.append(meta_type)
        root.set_silva_addables_allowed_in_container(addables)


def setupService(root):
    """instanciate service in root
    """
    if 'service_find' not in root.objectIds():
        factory = root.manage_addProduct['SilvaFind']
        factory.manage_addFindService('service_find')


def checkIndexes(root):
    """check that all searchSchema fields are indexed
    """
    catalog = getUtility(ICatalogService)
    indexes = set(catalog.indexes())
    for field in getUtility(IFindService).getSearchSchema().getFields():
        field_index = field.getIndexId()
        if field_index not in indexes:
            raise ValueError(
                u'Name "%s" not indexed by the catalog' % field_index)

