# -*- coding: utf-8 -*-
# Copyright (c) 2010-2013 Infrae. All rights reserved.
# See also LICENSE.txt

from Products.SilvaFind.i18n import translate as _

from Products.SilvaFind.results import MetatypeResultField
from Products.SilvaFind.results import LinkResultField
from Products.SilvaFind.results import DateResultField
from Products.SilvaFind.results import BreadcrumbsResultField
from Products.SilvaFind.results import FullTextResultField
from Products.SilvaFind.results import ThumbnailResultField
from Products.SilvaFind.results import ResultCountField
from Products.SilvaFind.results import RankingResultField
from Products.SilvaFind.results import AutomaticMetaDataResultField
from Products.SilvaFind.results import TotalResultCountField

from Products.SilvaFind.criterion import FullTextCriterionField
from Products.SilvaFind.criterion import MetatypeCriterionField
from Products.SilvaFind.criterion import PathCriterionField
from Products.SilvaFind.criterion import AutomaticMetaDataCriterionField


globalSearchFields= [
    MetatypeCriterionField(),
    FullTextCriterionField(),
    AutomaticMetaDataCriterionField(),
    PathCriterionField(),
    ]

globalResultsFields = [
    RankingResultField('',      _('Ranking'),
                                _('Full text result ranking')),
    TotalResultCountField('',   _('TotalResultCount'),
                                _('Show total number of results')),
    ResultCountField('',        _('ResultCount'),
                                _('Search result count')),
    MetatypeResultField('',     _('Icon'),
                                _('Display the icon of the content type.')),
    LinkResultField('',         _('Link')),
    DateResultField('',         _('Date')),
    FullTextResultField('',     _('Text snippet'),),
    ThumbnailResultField('',    _('Thumbnail')),
    AutomaticMetaDataResultField(),
    BreadcrumbsResultField('',  _('Breadcrumbs')),
    ]
