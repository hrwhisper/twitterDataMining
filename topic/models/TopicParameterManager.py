# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/18.


class TopicParameterManager(object):
    def __init__(self, param):
        param = dict(param)
        for x, t in param.items():
            if param[x] == '':
                del param[x]

        self.mode = int(param.get('mode', 1))

        # ---------- stream ---------
        self.track = param.get('track', None)
        self.follow = param.get('follow', None)
        self.location = param.get('location', None)
        self.storeIntoDB = param.get('storeIntoDB', False) == 'true'
        self.storeIntoDBName = param.get('storeIntoDBName', 'stream')

        # ---------- LDA ------------
        self.LDA_k = param.get('LDA_k', 15)
        self.LDA_timeWindow = param.get('LDA_timeWindow', 30)

        # ----------- Local -----------
        self.startDate = param.get('startDate', None)
        self.endDate = param.get('endDate', None)
        self.localCollectionsName = param.get('localCollectionsName', 'stream')

    def __eq__(self, other):
        return self.track == other.track and self.follow == other.follow and self.location == other.location \
               and self.storeIntoDB == other.storeIntoDB and self.storeIntoDBName == other.storeIntoDBName \
               and self.LDA_k == other.LDA_k and self.LDA_timeWindow == other.LDA_timeWindow \
               and self.startDate == other.startDate and self.endDate == other.endDate \
               and self.localCollectionsName == other.localCollectionsName and self.mode == other.mode

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.track, self.follow, self.location, self.storeIntoDB, self.storeIntoDBName, \
               self.LDA_k, self.LDA_timeWindow, self.startDate, self.endDate, self.localCollectionsName
