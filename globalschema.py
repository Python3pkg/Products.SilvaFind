from Products.Silva.i18n import translate as _

from Products.SilvaFind.schema import IconResultField, LinkResultField
from Products.SilvaFind.schema import PublicationDateResultField, BreadcrumbsResultField
from Products.SilvaFind.schema import ResultField, FullTextResultField 
from Products.SilvaFind.schema import ThumbnailResultField                               
from Products.SilvaFind.schema import ResultCountField
from Products.SilvaFind.schema import MetadataResultField
from Products.SilvaFind.schema import RankingResultField

from Products.SilvaFind.schema import FullTextCriterionField
from Products.SilvaFind.schema import MetatypeCriterionField
from Products.SilvaFind.schema import PathCriterionField

globalSearchFields= [
    MetatypeCriterionField(),
    FullTextCriterionField(),
    PathCriterionField(),
    ]
   
globalResultsFields = [
    RankingResultField('',      _(u'Ranking'),
                                _(u'full text result ranking')),
    ResultCountField('',        _(u'ResultCount'),
                                _(u'search result count')),
    IconResultField('',         _(u'Icon'), 
                                _(u'Display the icon of the content type.')),
    LinkResultField('',         _(u'Link')),
    PublicationDateResultField('', _(u'Publication Date')),
    FullTextResultField('',     _(u'Text snippet'),),
    ThumbnailResultField('',    _(u'Thumbnail')),
    BreadcrumbsResultField('',  _(u'Breadcrumbs')),
    ]
