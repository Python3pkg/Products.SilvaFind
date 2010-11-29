from Products.SilvaFind.i18n import translate as _

from Products.SilvaFind.schema import IconResultField, LinkResultField
from Products.SilvaFind.schema import DateResultField, BreadcrumbsResultField
from Products.SilvaFind.schema import FullTextResultField
from Products.SilvaFind.schema import ThumbnailResultField
from Products.SilvaFind.schema import ResultCountField
from Products.SilvaFind.schema import RankingResultField
from Products.SilvaFind.schema import AutomaticMetaDataResultField
from Products.SilvaFind.schema import TotalResultCountField

from Products.SilvaFind.schema import FullTextCriterionField
from Products.SilvaFind.schema import MetatypeCriterionField
from Products.SilvaFind.schema import PathCriterionField
from Products.SilvaFind.schema import AutomaticMetaDataCriterionField

globalSearchFields= [
    MetatypeCriterionField(),
    FullTextCriterionField(),
    AutomaticMetaDataCriterionField(),
    PathCriterionField(),
    ]

globalResultsFields = [
    RankingResultField('',      _(u'Ranking'),
                                _(u'full text result ranking')),
    TotalResultCountField('',   _(u'TotalResultCount'),
                                _(u'Show total number of results')),
    ResultCountField('',        _(u'ResultCount'),
                                _(u'search result count')),
    IconResultField('',         _(u'Icon'),
                                _(u'Display the icon of the content type.')),
    LinkResultField('',         _(u'Link')),
    DateResultField('', _(u'Date')),
    FullTextResultField('',     _(u'Text snippet'),),
    ThumbnailResultField('',    _(u'Thumbnail')),
    AutomaticMetaDataResultField(),
    BreadcrumbsResultField('',  _(u'Breadcrumbs')),
    ]
