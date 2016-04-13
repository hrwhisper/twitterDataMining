# -*- coding:utf-8 -*-

# Created by hrwhisper on 2015/12/10.
import pymongo
import datetime

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    # long running

    client = pymongo.MongoClient()
    db = client.twitter

    cursor = db.stream.aggregate([
        {
            '$match': {
                'entities.hashtags': 'MTVStars'
            }
        },
        {
            '$group': {
                '_id': {
                    'day': {'$dayOfMonth': '$created_at'},
                    'month': {'$month': '$created_at'},
                    'year': {'$year': '$created_at'}
                },
                'cnt': {'$sum': 1},
            }
        },
    ]);

    for i , group in enumerate(cursor):
        print i,group

    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds
