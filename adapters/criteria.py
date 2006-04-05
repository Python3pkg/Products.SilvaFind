
class SilvaFindError(Exception):
    pass

class Storage:
    def __init__(self, field, searchObject):
        self.field = field
        self.searchObject = searchObject
        
