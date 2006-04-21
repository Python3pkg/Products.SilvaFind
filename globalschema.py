from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema

from Products.SilvaFind.schema import ResultField
from Products.SilvaFind.schema import FullTextCriteriaField
from Products.SilvaFind.schema import MetadataCriteriaField

globalSearchSchema = SearchSchema([
    FullTextCriteriaField(),
    MetadataCriteriaField('silva-content', 'maintitle'),
    MetadataCriteriaField('silva-content', 'shorttitle'),
    ])
   
globalResultsSchema = ResultsSchema([
    ResultField('get_title'),
    ])
