# Copyright (c) 2006-2009 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: SilvaFind.py 33006 2009-01-13 12:31:43Z sylvain $

from zope.interface import Interface
from Products.Silva import interfaces

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
    '''
    Mapping between schema results field and ZCatalog metadata column
    '''
    def getColumnId():
        '''returns id of resultfield
        '''

    def getColumnTitle():
        '''returns title of resultfield
        '''

    def render(context, item):
        '''renders result field for item
        '''

