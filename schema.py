# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import re

from zope.interface import implements
from Products.SilvaFind import interfaces

# XXX: The Schema and BaseMetadata criterion have been changed back to
# old style classes because the unpickling is different and it breaks
# if the inherit from object

_marker = object()

class Schema:
    implements(interfaces.ISchema)

    def __init__(self, fields):
        self.fields = fields

    def getField(self, name, default=_marker):
        for field in self.fields:
            if field.getName() == name:
                return field
        if default is _marker:
            raise KeyError(name)
        return default

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


# BBB
from Products.SilvaFind.results.results import ResultField
from Products.SilvaFind.results.results import MetatypeResultField
from Products.SilvaFind.results.results import RankingResultField
from Products.SilvaFind.results.results import TotalResultCountField
from Products.SilvaFind.results.results import ResultCountField
from Products.SilvaFind.results.results import LinkResultField
from Products.SilvaFind.results.results import DateResultField
from Products.SilvaFind.results.results import ThumbnailResultField
from Products.SilvaFind.results.results import FullTextResultField
from Products.SilvaFind.results.results import BreadcrumbsResultField
from Products.SilvaFind.results.results import MetadataResultField
from Products.SilvaFind.results.results import AutomaticMetaDataResultField

IconResultField = MetatypeResultField
