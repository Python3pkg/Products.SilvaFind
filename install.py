"""Install for Silva Find
"""

# zope3
from zope.component import getMultiAdapter

# Silva
from Products.Silva.install import add_fss_directory_view

# SilvaFind
from Products.SilvaFind.adapters.interfaces import IIndexedField


def install(root):
    # create the core views from filesystem
    add_fss_directory_view(root.service_resources,
                           'SilvaFind', __file__, 'resources')

    # security
    root.manage_permission('Add Silva Finds',
                           ['Editor', 'ChiefEditor', 'Manager'])

    root.service_metadata.addTypesMapping(
        ('Silva Find', ), ('silva-content', 'silva-extra'))

    setupService(root)
    checkIndexes(root)
    configureAddables(root)


def uninstall(root):
    root.service_resources.manage_delObjects(['SilvaFind'])
    root.manage_delObjects(['service_find'])


def is_installed(root):
    return hasattr(root, 'service_find')


def configureAddables(root):
    addables = ['Silva Find']
    new_addables = root.get_silva_addables_allowed_in_container()
    for a in addables:
        if a not in new_addables:
            new_addables.append(a)
    root.set_silva_addables_allowed_in_container(new_addables)


def setupService(root):
    """instanciate service in root
    """
    if 'service_find' not in root.objectIds():
        factory = root.manage_addProduct['SilvaFind']
        factory.manage_addFindService('service_find')


def checkIndexes(root):
    """check that all searchSchema fields are indexed
    """

    for field in root.service_find.getSearchSchema().getFields():
        indexedField = getMultiAdapter((field, root), IIndexedField)
        indexedField.checkIndex()

