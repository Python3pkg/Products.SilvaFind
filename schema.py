import re

from zope.interface import implements

from Products.Silva.ViewCode import ViewCode
from Products.Silva.interfaces import IVersion
from Products.SilvaFind.interfaces import IMetadataCriterionField
from Products.SilvaFind.interfaces import IDateRangeMetadataCriterionField
from Products.SilvaFind.interfaces import IIntegerRangeMetadataCriterionField
from Products.SilvaFind.interfaces import IFullTextCriterionField
from Products.SilvaFind.interfaces import IPathCriterionField
from Products.SilvaFind.interfaces import IResultField
from Products.SilvaFind.interfaces import IMetatypeCriterionField
from Products.Silva.i18n import translate as _

class Schema:
    def __init__(self, fields):
        self.fields = fields

    def getFields(self):
        return self.fields

    def hasField(self, name):
        return name in self.getFieldNames()

    def getFieldNames(self):
        return [field.getName() for field in self.getFields()]

class SearchSchema(Schema):
   pass 

class ResultsSchema(Schema):
   pass 

class BaseMetadataCriterionField:

    def __init__(self, metadataSet, metadataId):
        self.metadataSet = metadataSet
        self.metadataId = metadataId

    def getMetadataSet(self):
        return self.metadataSet

    def getMetadataId(self):
        return self.metadataId

    def getName(self):
        return "%s-%s" % (self.getMetadataSet(), self.getMetadataId())

class MetadataCriterionField(BaseMetadataCriterionField):
    implements(IMetadataCriterionField)

class DateRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(IDateRangeMetadataCriterionField)

class IntegerRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(IIntegerRangeMetadataCriterionField)

class FullTextCriterionField:
    implements(IFullTextCriterionField)

    def getName(self):
        return "fulltext"

class MetatypeCriterionField:
    implements(IMetatypeCriterionField)
    
    def getName(self):
        return "meta_type"
    
class PathCriterionField:
    implements(IPathCriterionField)
    
    def getName(self):
        return "path"
    
class ResultField(object):
    implements(IResultField)
    
    def __init__(self, id, title, description=''):
        self.id = id
        self.title = title
        self.description = description

    def getName(self):
        return re.compile('[^a-z]').sub('', self.title.lower())

    def getColumnId(self):
        return self.id

    def getColumnTitle(self):
        return self.title

    def render(self, context, item):
        value = getattr(item.getObject(), self.id)()
        if not value:
            return
            
        if hasattr(value, 'strftime'): 
            # what the hell are these things?, 
            # they don't have a decent type            
            value = value.strftime('%d %b %Y %H:%M')

        value = '<span class="searchresult-field-value">%s</span>' % value
        title = '<span class="searchresult-field-title">%s</span>' % self.title
        return '<span class="searchresult-field">%s%s</span>' % (title, value)

class MetatypeResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        the_object = item.getObject()
        if IVersion.providedBy(the_object):
            the_object = the_object.object()
        return context.render_icon_by_meta_type(
            getattr(the_object, 'meta_type'))    

class ResultCountField(ResultField):
    implements(IResultField)
    description='search result count'
    def render(self, context, item):
        # the actual count is calculated in the pagetemplate
        # this is only here, so it can be enabled / disabled
        # in the smi.
        return 

class LinkResultField(ResultField):
    implements(IResultField)
    def render(self, context, item):
        url = item.silva_object_url
        title = item.getObject().get_title_or_id()
        return '<a href="%s" class="searchresult-link">%s</a>' % (url, title)
    
class PublicationDateResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        object = item.getObject()
        date = None
        if object.meta_type == 'Silva Document Version':
            date = object.get_approved_version_publication_datetime()
        if date == None:
            date = object.get_modification_datetime()
        datestr = date.strftime('%d %b %Y %H:%M').lower()
        
        return '<span class="searchresult-modified">%s</span>' % datestr
    
class ThumbnailResultField(ResultField):
     implements(IResultField)

     description = _('Shows thumbnails for images')

     
     def render(self, context, item):
        object = item.getObject()

        if object.meta_type != 'Silva Image':
            return

        if object.thumbnail_image is None:
            return

        url = item.silva_object_url
        img = object.thumbnail_image.tag()
        anchor = '<a href="%s">%s</a>' % (url, img)
        return '<div class="searchresult-thumbnail">%s</div>' % anchor
                     
        
class FullTextResultField(ResultField):
    implements(IResultField)

    description = _('Add text snippets from content')

    def render(self, context, item):
        object = item.getObject()
        ellipsis = '&#8230;'
        maxwords = 40
        searchterm = unicode(item.REQUEST.form.get('fulltext', ''), 'utf8')
        catalog = context.service_catalog
        fulltext = catalog.getIndexDataForRID(item.getRID()).get('fulltext', [])
        
        if not fulltext:
            # no fulltext available, probably an image
            return ''

        # since fulltext always starts with title, lets remove that
        fulltext = fulltext[len(object.get_title().split()):]
        
        searchterms = searchterm.split()
        if not searchterms:
            # searchterm is not specified,
            # return the first 20 words
            text = ' '.join(fulltext[:maxwords])
            if len(fulltext) > maxwords:
                text += ' ' + ellipsis
        else:
            words = maxwords / len(searchterms)
            text = []
            lowestpos = len(fulltext)
            highestpos = 0
            for term in searchterms:
                if not term in fulltext:
                    # term matched probably something in the title
                    # return the first n words:
                    line = ' '.join(fulltext[:words])
                    text.append(line)
                    lowestpos = 0
                    highestpos = words
                    continue

                pos = fulltext.index(term)
                if pos < lowestpos:
                    lowestpos = pos
                if pos > highestpos:
                    highestpos = pos
                start = pos -(words/2)
                end = pos + (words/2) + 1
                if start < 0 : 
                    end += -start
                    start = 0
                    
                pre = ' '.join(fulltext[start:pos])
                post = ' '.join(fulltext[pos+1:end])
                
                if not text and start != 0:
                    # we're adding the first (splitted) result
                    # and it's not at the beginning of the fulltext
                    # lets add an ellipsis
                    pre = ellipsis + pre
                    
                
                text.append('%s %s %s %s' % (
                                pre,
                                fulltext[pos],
                                post,
                                ellipsis)
                            )
            # if all the terms that are found are close together,
            # then use this, otherwise, we would end
            # up with the same sentence for each searchterm
            # this code will create a new text result list, which
            # does not have 'split' results.
            if lowestpos < highestpos:
                if highestpos - lowestpos < maxwords:
                    padding = (maxwords-(highestpos - lowestpos ))/2
                    lowestpos -= padding
                    highestpos += padding
                    if lowestpos < 0:
                        highestpos += -lowestpos
                        lowestpos = 0
                    
                    text = fulltext[lowestpos:highestpos]
                    if not lowestpos == 0:
                        text[0] = '%s %s' % (ellipsis, text[0])
                    if highestpos < len(fulltext)-1:
                        text[-1] += ' %s' % ellipsis
            
            text = ' %s ' % ' '.join(text)
            # do some hiliting
            for term in searchterms:
                if term.startswith('"'):
                    term = term[1:]
                if term.endswith('"'):
                    term = term[:-1]
                text = text.replace(' %s ' % term , 
                                    ' <strong>%s</strong> ' % term)
        return '<div class="searchresult-description">%s</div>' % text.strip()
        
            

class BreadcrumbsResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        obj = item.getObject()
        result = []
        for crumb in obj.get_breadcrumbs()[:-1]:
            result.append('<a href="%s">%s</a>' % (crumb.silva_object_url(),
                                                   crumb.get_title_or_id()))
        result = '<span> &#183; </span>'.join(result)
        return '<span class="searchresult-breadcrumb">%s</span>' % result

class IconResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        object = item.getObject()
        if IVersion.providedBy(object):
            object = object.object()
        img = context.render_icon(object)
        return '<span class="searchresult-icon">%s</span>' % img
    
class MetadataResultField(ResultField):
    implements(IResultField)

    description = '(metadata field)'

    def setMetadataElement(self, el):
        self.element = el

    def getMetadataElement(self):
        return self.element

    def render(self, context, item):
        set, element = self.id.split(':')

        value = context.service_metadata.getMetadataValue(
                item.getObject(), set, element)

        value = self.getMetadataElement().renderView(value)

        if not value:
            return
        
        #if hasattr(value, 'strftime'): 
            # what the hell are these things?, 
            # they don't have a decent type            
            #value = value.strftime('%d %b %Y %H:%M')
        cssid = "metadata-%s-%s" % (set, element)
        result = [  '<span class="searchresult-field" id="%s">' % cssid,
        
                    '<span class="searchresult-field-title">',
                    _(self.title),
                    '</span>',
                    '<span class="searchresult-field-value">',
                    value,
                    '</span>',
                    '</span>']
        # we return a list here, so the pt. can iterate it, and self.title will
        # be translated.
        return result
    
