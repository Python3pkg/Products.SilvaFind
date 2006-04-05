# SilvaFind
from Products.SilvaFind.adapters.metadatacriteria import MetadataCriteriaView
from Products.SilvaFind.adapters.metadatacriteria import MetadataCriteriaStorage
from Products.SilvaFind.adapters.metadatacriteria import IndexedMetadataCriteria

from Products.SilvaFind.adapters.fulltextcriteria import FullTextCriteriaView
from Products.SilvaFind.adapters.fulltextcriteria import FullTextCriteriaStorage
from Products.SilvaFind.adapters.fulltextcriteria import IndexedFullTextCriteria

class CatalogMetadataSetup:
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)
