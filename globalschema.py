from Products.Silva.i18n import translate as _

from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema

from Products.SilvaFind.schema import ResultField
from Products.SilvaFind.schema import FullTextCriteriaField
from Products.SilvaFind.schema import MetadataCriteriaField
from Products.SilvaFind.schema import DateRangeMetadataCriteriaField

globalSearchSchema = SearchSchema([
    FullTextCriteriaField(),
    MetadataCriteriaField('silva-content', 'maintitle'),
    MetadataCriteriaField('silva-content', 'shorttitle'),
    DateRangeMetadataCriteriaField('silva-extra', 'publicationtime'),
    ])
   
globalResultsSchema = ResultsSchema([
    ResultField('get_title', _('Title')),
    ])
