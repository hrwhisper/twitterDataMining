# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/2/10.
import datetime
from collections import defaultdict, OrderedDict

from twitterDataMining.models import MongoDb, TimeCost


def get_hashtag_pie_data_by_date(date='2015-12-24'):
    db = MongoDb().getDB()
    lower_bound = datetime.datetime(2015, 12, 24)
    upper_bound = lower_bound + datetime.timedelta(days=1)
    cursor = db.stream.aggregate([
        {
            '$match': {
                'hashtags': {'$exists': "true"},
                'time': {
                    "$gt": lower_bound,
                    "$lt": upper_bound
                }
            }
        },
        {
            '$project': {
                "hashtags": 1
            }
        }
    ])
    res = defaultdict(int)
    for tweet in cursor:
        for hashtag in tweet['hashtags']:
            res[hashtag] += 1

    res = OrderedDict(sorted(res.items(), key=lambda x: x[1], reverse=True)[:20])
    return {
        'label_data': res.keys(),
        'name_value': [{'name': key, 'value': value} for key, value in res.items()]
    }


if __name__ == '__main__':
    print get_hashtag_pie_data_by_date("2015-12-24")
