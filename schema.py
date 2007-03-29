import re

from zope.interface import implements

from Products.ZCTextIndex.ParseTree import ParseError

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

class AutomaticMetaDataCriterionField(object):
    """This class is a marker to put in the schemalist.
    This class will automaticly be replaced in the list 
    with all possible metadata values
    """
    pass
    
class AutomaticMetaDataResultField(object):
    """This class is a marker to put in the schemalist.
    This class will automaticly be replaced in the list 
    with all possible metadata values
    """
    pass
class ResultField(object):
    implements(IResultField)
    
    def __init__(self, id='', title='', description=''):
        # XXX the empty default values can go in 1.2, but are needed
        # for now, otherwise somehow the manage_services screen is
        # broken.
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

class RankingResultField(ResultField):
    implements(IResultField)
    description='full text result ranking'

    def render(self, context, item):
        catalog = context.service_catalog
        index = catalog.Indexes['fulltext']
        query = context.REQUEST.form.get('fulltext')
        if not query:
            return 
        query = unicode(query, 'utf8')
        batch_start =  int(context.REQUEST.form.get('batch_start',0))
        batch_end = batch_start + 25
        try:
            rankings = index.query(query, batch_end)[0]
        except ParseError: 
            return
        if not rankings:
            return
        highest = rankings[0][1]/100.0
        RID = item.getRID()
        sitepath = '/'.join(context.get_root().getPhysicalPath())
        img = '<img alt="Rank" src="%s/globals/ranking.gif"/>' % sitepath
        for ranking in rankings[batch_start:]:
            if ranking[0] == RID:
                return '<span class="searchresult-ranking">%s %.1f%%</span>' % (
                            img, (ranking[1] / highest))

class TotalResultCountField(ResultField):
    implements(IResultField)
    description='total search result number'
    def render(self, context, item):
        # the actual count is calculated in the pagetemplate
        # this is only here, so it can be enabled / disabled
        # in the smi.

        # Please note that enabling that showing the total 
        # number of search results might be a security risk
        # since it can be figured out that certain objects
        # were ommitted from the search
        return

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
        object = item.getObject()
        if object.meta_type == 'Silva Document Version':
            url = object.aq_parent.absolute_url()
        else:
            url = object.absolute_url()
        title = item.getObject().get_title_or_id()
        ellipsis = '&#8230;'
        if len(title) > 50:
            title = title[:50] + ellipsis
        return '<a href="%s" class="searchresult-link">%s</a>' % (url, title)
    
class DateResultField(ResultField):
    implements(IResultField)

    def render(self, context, item):
        object = item.getObject()
        date = None
        if object.meta_type == 'Silva Document Version':
            date = object.publication_datetime()
        if date == None:
            date = object.get_modification_datetime()
        datestr = date.strftime('%d %b %Y %H:%M').lower()
        
        return '<span class="searchresult-date">%s</span>' % datestr
    
class ThumbnailResultField(ResultField):
     implements(IResultField)

     description = _('Shows thumbnails for images')

     
     def render(self, context, item):
        object = item.getObject()

        if object.meta_type != 'Silva Image':
            return

        if object.thumbnail_image is None:
            return

        url = item.getURL()
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

        # since fulltext always starts with id and title, lets remove that
        idstring = object.id
        if object.meta_type == 'Silva Document Version':
            idstring = object.object().id
        skipwords = len(('%s %s' % (idstring, object.get_title())).split(' '))
        fulltext = fulltext[skipwords:]
        fulltextstr = ' '.join(fulltext)
        
        searchterms = searchterm.split()
        
        if not searchterms:
            # searchterm is not specified,
            # return the first 20 words
            text = ' '.join(fulltext[:maxwords])
            if object.meta_type == 'Silva Document Version':
                realtext = ' '.join(object.fulltext()[2:])
                # replace multiple whitespace characters with one space
                realtext = re.compile('[\ \n\t\xa0]+').sub(' ', realtext)
                text = ' '.join(realtext.split()[:maxwords])
            if len(fulltext) > maxwords:
                text += ' ' + ellipsis
        else:
            words = maxwords / len(searchterms)
            text = []
            lowestpos = len(fulltext)
            highestpos = 0
            
            hilite_terms = []
            for searchterm in searchterms:
                term = re.escape(searchterm)
                
                if '?' in term or '*' in term:
                    termq = term.replace('\\?', '.')
                    termq = termq.replace('\\*', '.[^\ ]*')
                    term_found = re.compile(termq).findall(fulltextstr)
                    if term_found:
                        hilite_terms += term_found
                        searchterms.remove(searchterm)
                        term = term_found[0]
                        searchterms.append(term.strip())
                    else:
                        hilite_terms.append(term)
                else:
                    hilite_terms.append(term)
                    
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
            
            # do some hiliting, use original text
            # (with punctuation) if this is a silva document
            text = ' '.join(text)
            if object.meta_type == 'Silva Document Version':
                realtext = ' '.join(object.fulltext()[2:])
                # replace multiple whitespace characters with one space
                realtext = re.compile('[\ \n\t\xa0]+').sub(' ', realtext)
                textparts = text.split(ellipsis)
                new = []
                for textpart in textparts:
                    if textpart == '':
                        new.append('')
                        continue
                    textpart = textpart.strip()
                    find = textpart.replace(' ', '[^a-zA-Z0-9]+')
                    textexpr = re.compile(find, re.IGNORECASE)
                    text = textexpr.findall(realtext)
                    if text:
                        text = text[0]
                    else:
                        # somehow we can't find a match in original text
                        # use the one from the catalog
                        text = textpart
                    new.append(text)
                text = ellipsis.join(new)

            for term in hilite_terms:
                if term.startswith('"'):
                    term = term[1:]
                if term.endswith('"'):
                    term = term[:-1]
                term = re.escape(term)
                text = ' ' + text
                regexp = re.compile('([^a-zA-Z0-9]+)(%s)([^a-zA-Z0-9]+)' % term.lower(), re.IGNORECASE)
                sub = '\g<1><strong class="search-result-snippet-hilite">\g<2></strong>\g<3>'
                text = regexp.sub(sub, text)
        return '<div class="searchresult-snippet">%s</div>' % text.strip()
        
            

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
        result = [  '<span class="searchresult-field %s">' % cssid,
        
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
    
