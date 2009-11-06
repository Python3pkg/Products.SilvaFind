try:
    from App.class_init import InitializeClass # Zope 2.12
except ImportError:
    from Globals import InitializeClass # Zope < 2.12

# Zope
from AccessControl import ClassSecurityInfo
from Acquisition import Implicit

# Silva
from Products.Silva import SilvaPermissions
from Products.SilvaFind.i18n import translate as _

# SilvaFind
from Products.SilvaFind.adapters.criterion import StoreCriterion
from Products.SilvaFind.errors import SilvaFindError


def convertValue(value):
    """Convert a value from what you get from the REQUEST to something
    working correctly with the catalog.
    """
    if not value:
        return u''
    if type(value) != type([]):
        return unicode(value, 'UTF-8')
    return [unicode(vl, 'UTF-8') for vl in value if vl] or u''


class StoreMetatypeCriterion(StoreCriterion):
    def store(self, REQUEST):
        #XXX some room for refactoring here
        field_name = self.criterion.getName()
        criterion_value = convertValue(REQUEST.get(field_name, None))
        self.query.setCriterionValue(field_name, criterion_value)


class MetatypeCriterionView(Implicit):

    security = ClassSecurityInfo()

    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'canBeShown')
    def canBeShown(self):
        return True

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderEditWidget')
    def renderEditWidget(self):
        value = self.getStoredValue()
        return self.renderWidget(value)

    security.declareProtected(SilvaPermissions.View,
        'renderPublicWidget')
    def renderPublicWidget(self):
        value = self.getValue(self.query.REQUEST)
        select_all_text = _('All Types')
        return {'value': value,
                'name': self.criterion.getName(),
                'meta_types': self.getAvailableMetaTypes(),
                'field_type': self.__class__.__name__,
                'select_all_text': select_all_text,}

    security.declareProtected(SilvaPermissions.ChangeSilvaContent,
        'renderWidget')
    def renderWidget(self, value):
        if value is None:
            value = ''

        html = '<select class="store" multiple="multiple" name="%s:list" id="%s" size="5"> ' % (self.criterion.getName(),
                            self.criterion.getName())
        selected = ''
        if not value:
            selected = ' selected="selected"'
        select_all_text = _('All Types')
        meta_types = ['<option value=""%s>%s</option>' % (selected,
                                                          select_all_text)]
        for meta_type in self.getAvailableMetaTypes():
            selected = ''
            if meta_type in value:
                selected = ' selected="selected"'
            name = meta_type.replace('Silva ', '')
            meta_types.append('<option value="%s"%s>%s</option>' % (meta_type,
                                                                    selected,
                                                                    name))
        html += '\n'.join(meta_types)
        html += '</select>'
        return html

    security.declareProtected(SilvaPermissions.View, 'getValue')
    def getValue(self, REQUEST):
        field_name = self.criterion.getName()
        value = REQUEST.get(field_name, None)
        if value:
            return convertValue(value)
        return self.getStoredValue()

    getIndexValue = getValue

    def getAvailableMetaTypes(self):
        return self.query.service_catalog.uniqueValuesFor(
            self.getIndexId())

    security.declareProtected(SilvaPermissions.View, 'getStoredValue')
    def getStoredValue(self):
        return self.query.getCriterionValue(self.criterion.getName())

    security.declareProtected(SilvaPermissions.View, 'getTitle')
    def getTitle(self):
        return 'content type'

    def getIndexId(self):
        return 'meta_type'

    security.declareProtected(SilvaPermissions.View, 'getName')
    def getName(self):
        return self.criterion.getName()

    security.declareProtected(SilvaPermissions.View, 'getDescription')
    def getDescription(self):
        return _('Search for the selected content types.')

InitializeClass(MetatypeCriterionView)

class IndexedMetatypeCriterion:
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        return 'meta_type'

    def checkIndex(self):
        id = self.getIndexId()
        if id not in self.catalog.indexes():
            raise SilvaFindError('Name "%s" not indexed by service_catalog' % id)
