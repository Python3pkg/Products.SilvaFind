# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from App.class_init import InitializeClass

# Silva
from Products.Silva import SilvaPermissions


class ResultView(Implicit):

    security = ClassSecurityInfo()

    def __init__(self, result, query):
        self.result = result
        self.query = query

    security.declareProtected(SilvaPermissions.View,
        'getTitle')
    def getTitle(self):
        return self.result.getColumnTitle().lower()

    security.declareProtected(SilvaPermissions.View,
        'getId')
    def getId(self):
        return self.result.getColumnId()

    security.declareProtected(SilvaPermissions.View,
        'getName')
    def getName(self):
        return self.result.getName()

    security.declareProtected(SilvaPermissions.View,
        'getDescription')
    def getDescription(self):
        return self.result.description

    security.declareProtected(SilvaPermissions.View,
        'render')
    def render(self, context, item, request):
        return self.result.render(context, item, request)

InitializeClass(ResultView)
