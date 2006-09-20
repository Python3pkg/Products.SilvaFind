from Products.Silva.i18n import translate as _

from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema

from Products.SilvaFind.schema import ResultField
from Products.SilvaFind.schema import FullTextCriterionField
from Products.SilvaFind.schema import MetadataCriterionField
from Products.SilvaFind.schema import MetatypeCriterionField
from Products.SilvaFind.schema import DateRangeMetadataCriterionField

globalSearchSchema = SearchSchema([
    FullTextCriterionField(),
    MetatypeCriterionField(),
    MetadataCriterionField('silva-content', 'maintitle'),
    MetadataCriterionField('silva-content', 'shorttitle'),
    DateRangeMetadataCriterionField('silva-extra', 'publicationtime'),
    ])
   
globalResultsSchema = ResultsSchema([
    ResultField('get_title', _('Title')),
    ])
