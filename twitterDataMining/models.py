# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/2/5.
import datetime
import pymongo


class MongoDb(object):
    def __init__(self):
        self._client = pymongo.MongoClient()
        self.db = self._client.twitter2

    def getDB(self):
        return self.db


class TimeCost(object):
    def __init__(self):
        self._start_time = datetime.datetime.now()

    def timecost(self):
        print datetime.datetime.now() - self._start_time
