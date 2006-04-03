#Silva
from Products.Silva.fssite import registerDirectory


#SilvaFind
from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema
from Products.SilvaFind.schema import MetadataField
from Products.SilvaFind.schema import ResultField

globalSearchSchema = SearchSchema([
    MetadataField('silva-content', 'maintitle'),
    MetadataField('silva-content', 'shorttitle'),
    ])

globalResultsSchema = ResultsSchema([
    ResultField('get_title'),
    ])

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
    from Products.SilvaFind.interfaces import IMetadataSearchField
    from Products.SilvaFind.interfaces import ISearchFieldView
    from Products.SilvaFind.interfaces import ISearchObject
    from Products.SilvaFind.interfaces import IQueryPart
    from Products.SilvaFind.interfaces import IIndexedField
    from Products.SilvaFind.adapters import MetadataFieldView
    from Products.SilvaFind.adapters import MetadataIndexedField 

    Adapters = zapi.getService(zapi.servicenames.Adapters)
    Adapters.register((IMetadataSearchField, ISearchObject), ISearchFieldView, '',
       MetadataFieldView)
    Adapters.register((IMetadataSearchField, ISearchObject), IQueryPart, '',
       MetadataFieldView)
    Adapters.register((IMetadataSearchField, IRoot), IIndexedField, '',
       MetadataIndexedField)


def register_type_for_metadata():
    """
    register the silva core content types with the metadata system
    """
    from Products.SilvaFind.SilvaFind import SilvaFind
    from Products.Silva.Metadata import registerTypeForMetadata
    
    registerTypeForMetadata(SilvaFind.meta_type)
