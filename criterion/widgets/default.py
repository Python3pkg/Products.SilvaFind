# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

class StoreCriterion(object):

    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query


class IndexedCriterion(object):
    def __init__(self, criterion, root):
        self.criterion = criterion
        self.root = root
        self.catalog = root.service_catalog

    def getIndexId(self):
        raise NotImplementedError

    def checkIndex(self):
        index = self.getIndexId()
        if index not in self.catalog.indexes():
            raise ValueError(u'Name "%s" not indexed by the catalog' % index)


class CatalogMetadataSetup(object):

    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)

