# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import re

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.traversing.browser.interfaces import IAbsoluteURL

from Products.ZCTextIndex.ParseTree import ParseError

from silva.core.interfaces import IVersion, IPublishable
from Products.SilvaFind import interfaces
from Products.SilvaFind.i18n import translate as _

# XXX: The Schema and BaseMetadata criterion have been changed back to
# old style classes because the unpickling is different and it breaks
# if the inherit from object


class Schema:
    implements(interfaces.ISchema)

    def __init__(self, fields):
        self.fields = fields

    def getField(self, name):
        for field in self.fields:
            if field.getName() == name:
                return field
        raise KeyError(name)

    def getFields(self):
        return self.fields

    def hasField(self, name):
        return name in self.getFieldNames()

    def getFieldNames(self):
        return [field.getName() for field in self.getFields()]


class SearchSchema(Schema):
    implements(interfaces.ISearchSchema)


class ResultsSchema(Schema):
    implements(interfaces.IResultsSchema)


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
    implements(interfaces.IMetadataCriterionField)


class DateRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(interfaces.IDateRangeMetadataCriterionField)


class IntegerRangeMetadataCriterionField(BaseMetadataCriterionField):
    implements(interfaces.IIntegerRangeMetadataCriterionField)


class FullTextCriterionField(object):
    implements(interfaces.IFullTextCriterionField)

    def getName(self):
        return "fulltext"


class MetatypeCriterionField(object):
    implements(interfaces.IMetatypeCriterionField)

    def getName(self):
        return "meta_type"


class PathCriterionField(object):
    implements(interfaces.IPathCriterionField)

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
    implements(interfaces.IResultField)

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

    def render(self, context, item, request):
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

    def render(self, context, item, request):
        the_object = item.getObject()
        if IVersion.providedBy(the_object):
            the_object = the_object.object()
        return context.render_icon_by_meta_type(
            getattr(the_object, 'meta_type'))


class RankingResultField(ResultField):
    description=_('full text result ranking')

    def render(self, context, item, request):
        catalog = context.service_catalog
        index = catalog.Indexes['fulltext']
        query = request.form.get('fulltext')
        if not query:
            return
        query = unicode(query, 'utf8')
        batch_start =  int(request.form.get('batch_start',0))
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
    description=_('total search result number')

    def render(self, context, item, request):
        # the actual count is calculated in the pagetemplate
        # this is only here, so it can be enabled / disabled
        # in the smi.

        # Please note that enabling that showing the total
        # number of search results might be a security risk
        # since it can be figured out that certain objects
        # were ommitted from the search
        return None

class ResultCountField(ResultField):
    description=_('search result count')

    def render(self, context, item, request):
        # the actual count is calculated in the pagetemplate
        # this is only here, so it can be enabled / disabled
        # in the smi.
        return


class LinkResultField(ResultField):

    def render(self, context, item, request):
        content = item.getObject()
        title = content.get_title_or_id()
        if IVersion.providedBy(content):
            url = absoluteURL(content.get_content(), request)
        else:
            url = absoluteURL(content, request)
        ellipsis = '&#8230;'
        if len(title) > 50:
            title = title[:50] + ellipsis
        return '<a href="%s" class="searchresult-link">%s</a>' % (url, title)


class DateResultField(ResultField):

    def render(self, context, item, request):
        content = item.getObject()
        date = None
        datestr = ''
        if IPublishable.providedBy(content):
            date = content.publication_datetime()
        if date == None:
            date = content.get_modification_datetime()
        if date and hasattr(date, 'strftime'):
            datestr = date.strftime('%d %b %Y %H:%M').lower()

        return '<span class="searchresult-date">%s</span>' % datestr


class ThumbnailResultField(ResultField):
     description = _('Shows thumbnails for images')

     def render(self, context, item, request):
        content = item.getObject()

        if content.meta_type != 'Silva Image':
            return

        if content.thumbnail_image is None:
            return

        url = item.getURL()
        img = content.thumbnail_image.tag()
        anchor = '<a href="%s">%s</a>' % (url, img)
        return '<div class="searchresult-thumbnail">%s</div>' % anchor


class FullTextResultField(ResultField):
    description = _('Add text snippets from content')

    def render(self, context, item, request):
        content = item.getObject()
        ellipsis = '&#8230;'
        maxwords = 40
        searchterm = unicode(request.form.get('fulltext', ''), 'utf8')
        catalog = context.service_catalog
        fulltext = catalog.getIndexDataForRID(item.getRID()).get('fulltext', [])

        if not fulltext:
            # no fulltext available, probably an image
            return ''

        # since fulltext always starts with id and title, lets remove that
        idstring = content.id
        if IVersion.providedBy(content):
            idstring = content.get_content().id
        skipwords = len(('%s %s' % (idstring, content.get_title())).split(' '))
        fulltext = fulltext[skipwords:]
        fulltextstr = ' '.join(fulltext)

        searchterms = searchterm.split()

        if not searchterms:
            # searchterm is not specified,
            # return the first 20 words
            text = ' '.join(fulltext[:maxwords])
            if IVersion.providedBy(content) and hasattr(content, 'fulltext'):
                realtext = ' '.join(content.fulltext()[2:])
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
            if IVersion.providedBy(content) and hasattr(content, 'fulltext'):
                realtext = ' '.join(content.fulltext()[2:])
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
                regexp = re.compile(
                    '([^a-zA-Z0-9]+)(%s)([^a-zA-Z0-9]+)' % term.lower(),
                    re.IGNORECASE)
                sub = ('\g<1><strong class="search-result-snippet-hilite">'
                       '\g<2></strong>\g<3>')
                text = regexp.sub(sub, text)
        return '<div class="searchresult-snippet">%s</div>' % text.strip()


class BreadcrumbsResultField(ResultField):

    def render(self, context, item, request):
        content = item.getObject()
        result = []
        breadcrumb = getMultiAdapter((content, request), IAbsoluteURL)
        for crumb in breadcrumb.breadcrumbs()[:-1]:
            result.append('<a href="%s">%s</a>' % (crumb['url'], crumb['name']))
        result = '<span> &#183; </span>'.join(result)
        return '<span class="searchresult-breadcrumb">%s</span>' % result


class IconResultField(ResultField):

    def render(self, context, item, request):
        content = item.getObject()
        if IVersion.providedBy(content):
            content = content.get_content()
        img = context.render_icon(content)
        return '<span class="searchresult-icon">%s</span>' % img


class MetadataResultField(ResultField):

    description = _('(metadata field)')

    def setMetadataElement(self, el):
        self.element = el

    def getMetadataElement(self):
        return self.element

    def render(self, context, item, request):
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

