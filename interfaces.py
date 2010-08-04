# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface
from silva.core import interfaces

"""
A query is a set of criterion.
A criterion is made both of an indexed field of content items
and of value(s) that will be searched for in the catalog.
"""


class IQuery(Interface):
    """Store values used by a query.
    """

    def getCriterionValue(name):
        """Returns stored value for the field named name.
        """

    def setCriterionValue(name, value):
        """Store the given value for the named name criterion.
        """

class IQueryPart(Interface):
    """Adaptor on a criterion, query and request to provide a piece of
    a full catalog query.
    """

    def getIndexId():
        """Catalog Index to be queried.
        """

    def getIndexValue():
        """Return the value to passe the Catalog Index for the query.
        """


class IFind(interfaces.IContent, IQuery):
    """A Silva find object.
    """


class IFindService(interfaces.ISilvaService):
    """Silva find service
    """

    def getSearchSchema():
        """Return the default search schema
        """

    def getResultsSchema():
        """Return the default result schema
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


class ICriterionData(Interface):
    """Manage access to stored criterion data.
    """

    def getValue():
        """Return the value.
        """

    def setValue(value):
        """Change criterion value.
        """

class ICriterionView(IQueryPart):
    """Render/extract value for a criterion for both data input and
    build a query (it is basically two different way to render a
    criterion).

    For data input, two widgets can be rendered:
    - edit view (default criterion value)
    - public view (value to be searched)
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


