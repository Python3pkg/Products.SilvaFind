# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from AccessControl import allow_module
from Products.FileSystemSite.DirectoryView import registerDirectory
from Products.SilvaFind import install
from silva.core import conf as silvaconf


silvaconf.extensionName('SilvaFind')
silvaconf.extensionTitle('Silva Find')

allow_module('Products.SilvaFind.i18n')

registerDirectory('views', globals())
registerDirectory('resources', globals())

