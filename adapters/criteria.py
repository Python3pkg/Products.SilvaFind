
class SilvaFindError(Exception):
    pass

class CriteriaStorage:
    def __init__(self, criteria, query):
        self.criteria = criteria
        self.query = query
        
