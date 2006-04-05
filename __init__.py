#Silva
from Products.Silva.fssite import registerDirectory

def initialize(context):
    from Products.Silva.ExtensionRegistry import extensionRegistry
    import SilvaFind
    import install
    
    registerDirectory('views', globals())
    
    extensionRegistry.register(
        'SilvaFind', 'Silva Find', context, [
        SilvaFind,
        ], install, depends_on='Silva')

    register_type_for_metadata()

    from zope.app import zapi
    from Products.Silva.interfaces import IRoot
    from Products.SilvaFind.interfaces import ICriteriaView
    from Products.SilvaFind.interfaces import ISilvaQuery
    from Products.SilvaFind.interfaces import IQueryPart
    from Products.SilvaFind.interfaces import IIndexedField
    from Products.SilvaFind.interfaces import IStoredCriteria

    Adapters = zapi.getService(zapi.servicenames.Adapters)
    
    from Products.SilvaFind.interfaces import ICatalogMetadataSetup
    from Products.SilvaFind.interfaces import IResultField
    from Products.SilvaFind.adapters import CatalogMetadataSetup
    Adapters.register((IResultField, IRoot), ICatalogMetadataSetup, '',
       CatalogMetadataSetup)
    
    from Products.SilvaFind.interfaces import IMetadataCriteriaField
    from Products.SilvaFind.adapters import MetadataCriteriaView
    from Products.SilvaFind.adapters import MetadataCriteriaStorage
    from Products.SilvaFind.adapters import IndexedMetadataCriteria 
    Adapters.register((IMetadataCriteriaField, ISilvaQuery), ICriteriaView, '',
       MetadataCriteriaView)
    Adapters.register((IMetadataCriteriaField, ISilvaQuery), IQueryPart, '',
       MetadataCriteriaView)
    Adapters.register((IMetadataCriteriaField, ISilvaQuery), IStoredCriteria, '',
       MetadataCriteriaStorage)
    Adapters.register((IMetadataCriteriaField, IRoot), IIndexedField, '',
       IndexedMetadataCriteria)
    
    from Products.SilvaFind.interfaces import IFullTextCriteriaField
    from Products.SilvaFind.adapters import FullTextCriteriaView
    from Products.SilvaFind.adapters import FullTextCriteriaStorage
    from Products.SilvaFind.adapters import IndexedFullTextCriteria
    Adapters.register((IFullTextCriteriaField, ISilvaQuery), ICriteriaView, '',
       FullTextCriteriaView)
    Adapters.register((IFullTextCriteriaField, ISilvaQuery), IQueryPart, '',
       FullTextCriteriaView)
    Adapters.register((IFullTextCriteriaField, ISilvaQuery), IStoredCriteria, '',
       FullTextCriteriaStorage)
    Adapters.register((IFullTextCriteriaField, IRoot), IIndexedField, '',
       IndexedFullTextCriteria)


def register_type_for_metadata():
    """
    register the silva core content types with the metadata system
    """
    from Products.SilvaFind.SilvaFind import SilvaFind
    from Products.Silva.Metadata import registerTypeForMetadata
    
    registerTypeForMetadata(SilvaFind.meta_type)
