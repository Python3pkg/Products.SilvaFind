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


class IMetadataCriterionField(Interface):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    '''
    def getMetadataSet():
        '''returns Silva MetadataSet id'''

    def getMetadataId():
        '''returns Silva MetadataSet element id'''


class IDateRangeMetadataCriterionField(IMetadataCriterionField):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    date
    '''


class IIntegerRangeMetadataCriterionField(IMetadataCriterionField):
    '''
    Criterion corresponding to indexed SilvaMetadata fields
    date
    '''


class IFullTextCriterionField(Interface):
    '''
    Criterion corresponding to the Silva full text index
    '''


class IMetatypeCriterionField(Interface):
    '''
    Criterion corresponding to the Silva Meta Type of an object
    '''


class IPathCriterionField(Interface):
    '''
    Criterion used to restrict searchresults so they start with a specific path
    '''


class IResultField(Interface):
    """This describe an included field to appear in the results. That
    can either a special field like a breadcrumb, the last
    modification time, a link to the content, or an arbitrary metadata
    field.
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


