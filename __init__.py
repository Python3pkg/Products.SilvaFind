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

def register_type_for_metadata():
    """
    register the silva core content types with the metadata system
    """
    from Products.SilvaFind.SilvaFind import SilvaFind
    from Products.Silva.Metadata import registerTypeForMetadata
    
    registerTypeForMetadata(SilvaFind.meta_type)
