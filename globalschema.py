from Products.Silva.i18n import translate as _

from Products.SilvaFind.schema import SearchSchema
from Products.SilvaFind.schema import ResultsSchema

from Products.SilvaFind.schema import ResultField
from Products.SilvaFind.schema import FullTextCriteriaField
from Products.SilvaFind.schema import MetadataCriteriaField

globalSearchSchema = SearchSchema([
    FullTextCriteriaField(),
    MetadataCriteriaField('silva-content', 'maintitle'),
    MetadataCriteriaField('silva-content', 'shorttitle'),
    MetadataCriteriaField('silva-extra', 'publicationtime'),
    ])
   
globalResultsSchema = ResultsSchema([
    ResultField('get_title', _('Title')),
    ResultField('get_publicationtime', _('Publication date')),
    ])
