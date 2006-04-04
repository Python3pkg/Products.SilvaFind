#Silva
from Products.Silva.fssite import registerDirectory


#SilvaFind
from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema
from Products.SilvaFind.schema import MetadataField
from Products.SilvaFind.schema import FullTextField
from Products.SilvaFind.schema import ResultField

globalSearchSchema = SearchSchema([
    FullTextField(),
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
    from Products.SilvaFind.interfaces import ICriteriaView
    from Products.SilvaFind.interfaces import ISilvaQuery
    from Products.SilvaFind.interfaces import IQueryPart
    from Products.SilvaFind.interfaces import IIndexedField
    from Products.SilvaFind.interfaces import IStoredCriteria

    Adapters = zapi.getService(zapi.servicenames.Adapters)
    
    from Products.SilvaFind.interfaces import IMetadataSearchField
    from Products.SilvaFind.adapters import MetadataFieldView
    from Products.SilvaFind.adapters import MetadataFieldStorage
    from Products.SilvaFind.adapters import MetadataIndexedField 
    Adapters.register((IMetadataSearchField, ISilvaQuery), ICriteriaView, '',
       MetadataFieldView)
    Adapters.register((IMetadataSearchField, ISilvaQuery), IQueryPart, '',
       MetadataFieldView)
    Adapters.register((IMetadataSearchField, ISilvaQuery), IStoredCriteria, '',
       MetadataFieldStorage)
    Adapters.register((IMetadataSearchField, IRoot), IIndexedField, '',
       MetadataIndexedField)
    
    from Products.SilvaFind.interfaces import IFullTextField
    from Products.SilvaFind.adapters import FullTextFieldView
    from Products.SilvaFind.adapters import FullTextFieldStorage
    from Products.SilvaFind.adapters import FullTextIndexedField
    Adapters.register((IFullTextField, ISilvaQuery), ICriteriaView, '',
       FullTextFieldView)
    Adapters.register((IFullTextField, ISilvaQuery), IQueryPart, '',
       FullTextFieldView)
    Adapters.register((IFullTextField, ISilvaQuery), IStoredCriteria, '',
       FullTextFieldStorage)
    Adapters.register((IFullTextField, IRoot), IIndexedField, '',
       FullTextIndexedField)


def register_type_for_metadata():
    """
    register the silva core content types with the metadata system
    """
    from Products.SilvaFind.SilvaFind import SilvaFind
    from Products.Silva.Metadata import registerTypeForMetadata
    
    registerTypeForMetadata(SilvaFind.meta_type)
