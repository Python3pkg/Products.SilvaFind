# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

class StoreCriterion(object):
    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query

class CatalogMetadataSetup(object):
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)

