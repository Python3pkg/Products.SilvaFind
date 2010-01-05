# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

#Silva
from Products.Silva.fssite import registerDirectory

from AccessControl import allow_module
from silva.core import conf as silvaconf

silvaconf.extensionName('SilvaFind')
silvaconf.extensionTitle('Silva Find')

allow_module('Products.SilvaFind.i18n')

import install

def initialize(context):
    registerDirectory('views', globals())
    registerDirectory('resources', globals())

