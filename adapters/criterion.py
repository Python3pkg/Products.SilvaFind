
class StoreCriterion:
    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query
        
class CatalogMetadataSetup:
    def __init__(self, field, root):
        self.field = field
        self.root = root
        self.catalog = root.service_catalog

    def setUp(self):
        id = self.field.getColumnId()
        if not id in self.catalog.schema():
            self.catalog.addColumn(id)
