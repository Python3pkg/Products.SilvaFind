from Globals import InitializeClass

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions

class ResultView(Implicit):

    security = ClassSecurityInfo()

    def __init__(self, result, query):
        self.result = result
        self.query = query
    
    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'getTitle')
    def getTitle(self):
        return self.result.getColumnTitle().lower()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'getId')
    def getId(self):
        return self.result.getColumnId()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'getName')
    def getName(self):
        return self.result.getName()

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'getDescription')
    def getDescription(self):
        return self.result.description

    security.declareProtected(SilvaPermissions.View,
        'render')
    def render(self, context, item):
        return self.result.render(context, item)

InitializeClass(ResultView)
