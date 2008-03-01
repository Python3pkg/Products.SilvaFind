#Silva
from Products.Silva.fssite import registerDirectory
import install

from AccessControl import allow_module

allow_module('Products.SilvaFind.i18n')

has_makeContainerFilter = True
try:
    from Products.Silva.helpers import makeContainerFilter
except:
    has_makeContainerFilter = False

def initialize(context):
    import findservice
    
    registerDirectory('views', globals())
    registerDirectory('resources', globals())

    if has_makeContainerFilter:
        context.registerClass(
            findservice.FindService,
            constructors = (findservice.manage_addFindService,),
            icon = "www/find.png",
            container_filter = makeContainerFilter()
            )
    else:
        context.registerClass(
            findservice.FindService,
            constructors = (findservice.manage_addFindService,),
            icon = "www/find.png"
            )
