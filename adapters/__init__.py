# SilvaFind
from Products.SilvaFind.adapters.metadatacriteria import MetadataFieldView
from Products.SilvaFind.adapters.metadatacriteria import MetadataFieldStorage
from Products.SilvaFind.adapters.metadatacriteria import MetadataIndexedField

from Products.SilvaFind.adapters.fulltextcriteria import FullTextFieldView
from Products.SilvaFind.adapters.fulltextcriteria import FullTextFieldStorage
from Products.SilvaFind.adapters.fulltextcriteria import FullTextIndexedField

class CatalogMetadataSetup:
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)
