# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from silva.core import interfaces

'''
A query is a set of criteria.
A criterion is made both of an indexed field of content items
and of value(s) that will be searched for in the catalog.
'''


class ISilvaQuery(Interface):
    '''Persistent query'''

    def getCriterionValue(schemaField):
        '''returns stored value for schemaField'''


class IFind(interfaces.IContent, ISilvaQuery):
    """A Silva find object.
    """


class IFindService(interfaces.ISilvaService):
    """Silva find service
    """

    def getSearchSchema():
        """Return a search schema.
        """

    def getResultsSchema():
        """Return a result schema.
        """


class ISchema(Interface):
    """A find schema.
    """

    def getFields():
        """Return fields of the schema.
        """

    def hasField(name):
        """Return True if there is field called name in the schema.
        """

    def getFieldNames():
        """Return a list of field names.
        """


class ISearchSchema(ISchema):
    """Search schema.
    """


class IResultsSchema(ISchema):
    """Result schema.
    """

# Search criterions

class ICriterionField(Interface):
    """A criterion describes a field that can be used in a search
    query.
    """

    def getName():
        """Return a unique name for the criterion.
        """

    def getTitle():
        """Return a title identifying the criterion.
        """

    def getDescription():
        """Return a description.
        """

    def getIndexId():
        """Return the index id in the catalog to do a search on this
        criterion.
        """


class IMetadataCriterionField(ICriterionField):
    """Criterion to search on an indexed metadata element.
    """

    def getSetName():
        """Return the set name of the metadata element
        """

    def getElementName():
        """Return the name of the element inside its set.
        """

    def getMetadataElement():
        """Return the metadata element.
        """


class IDateRangeMetadataCriterionField(IMetadataCriterionField):
    """Criterion to search an indexed metadata date element.
    """


class IIntegerRangeMetadataCriterionField(IMetadataCriterionField):
    """Criterion to search on a indexed range of integer.
    """


class IFullTextCriterionField(ICriterionField):
    """Criterion to do full text search.
    """


class IMetatypeCriterionField(ICriterionField):
    """Criterion to restrict the search to some Silva metatype.
    """


class IPathCriterionField(ICriterionField):
    """Criterion to restrict the search on content located inside an other.
    """


# Search results

class IResultField(Interface):
    """This describe a field which is able to appear in the
    results. That can either a special field like a breadcrumb, the
    last modification time, a link to the content, or an arbitrary
    metadata field.
    """

    def getId():
        """Gives the ID of this result field.
        """

    def getName():
        """Gives the name of this result field.
        """

    def getTitle():
        """Gives the title of this result field.
        """

    def getDescription():
        """Gives the description of this result field.
        """


class IResultView(Interface):
    """Render a ResultField for the public.
    """

    def __init__(context, result, request):
        """Build the view
        """

    def render(item):
        """renders result field for an item
        """


