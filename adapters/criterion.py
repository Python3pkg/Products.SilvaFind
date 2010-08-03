# Copyright (c) 2006-2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

class StoreCriterion(object):

    def __init__(self, criterion, query):
        self.criterion = criterion
        self.query = query


class CriterionView(object):

    def __init__(self, criterion, query, request):
        self.criterion = criterion
        self.query = query
        self.request = request

    def getTitle(self):
        return self.criterion.getTitle()

    def getIndexId(self):
        return self.criterion.getIndexId()

    def getDescription(self):
        return self.criterion.getDescription()

    def getName(self):
        return self.criterion.getName()
