# -*- coding: utf-8 -*-
# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from Products.SilvaFind.i18n import translate as _

from Products.SilvaFind.results.results import MetatypeResultField
from Products.SilvaFind.results.results import LinkResultField
from Products.SilvaFind.results.results import DateResultField
from Products.SilvaFind.results.results import BreadcrumbsResultField
from Products.SilvaFind.results.results import FullTextResultField
from Products.SilvaFind.results.results import ThumbnailResultField
from Products.SilvaFind.results.results import ResultCountField
from Products.SilvaFind.results.results import RankingResultField
from Products.SilvaFind.results.results import AutomaticMetaDataResultField
from Products.SilvaFind.results.results import TotalResultCountField

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
                                _(u'Full text result ranking')),
    TotalResultCountField('',   _(u'TotalResultCount'),
                                _(u'Show total number of results')),
    ResultCountField('',        _(u'ResultCount'),
                                _(u'Search result count')),
    MetatypeResultField('',         _(u'Icon'),
                                _(u'Display the icon of the content type.')),
    LinkResultField('',         _(u'Link')),
    DateResultField('', _(u'Date')),
    FullTextResultField('',     _(u'Text snippet'),),
    ThumbnailResultField('',    _(u'Thumbnail')),
    AutomaticMetaDataResultField(),
    BreadcrumbsResultField('',  _(u'Breadcrumbs')),
    ]
