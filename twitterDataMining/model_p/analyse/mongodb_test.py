# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/24.
import pymongo


class mongodbTest(object):
    def test(self):
        client = pymongo.MongoClient()
        db = client.twitter
        return db.stream.find().limit(10)
