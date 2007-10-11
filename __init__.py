#Silva
from Products.Silva.fssite import registerDirectory

from AccessControl import allow_module

allow_module('Products.SilvaFind.i18n')

def initialize(context):
    from Products.Silva.ExtensionRegistry import extensionRegistry
    import SilvaFind
    import findservice
    import install
    
    registerDirectory('views', globals())
    registerDirectory('resources', globals())
    
    extensionRegistry.register(
        'SilvaFind', 'Silva Find', context, [
        SilvaFind,
        ], install, depends_on='Silva')

    context.registerClass(
        findservice.FindService,
        constructors = (
            findservice.manage_addFindService,),
        icon = "www/find.png"
        )

    register_type_for_metadata()

def register_type_for_metadata():
    """
    register the silva core content types with the metadata system
    """
    from Products.SilvaFind.SilvaFind import SilvaFind
    from Products.Silva.Metadata import registerTypeForMetadata
    
    registerTypeForMetadata(SilvaFind.meta_type)
