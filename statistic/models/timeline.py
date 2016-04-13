# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/2/8.
import datetime

import collections

from twitterDataMining.models import MongoDb, TimeCost


def get_time_from_res_dict(res_time):
    temp = map(str, [res_time['year'], res_time['month'], res_time['day'], res_time['hour']])
    return '-'.join(temp[:3]) + ' ' + temp[3].zfill(2) + ":00"


def get_hashtag_group_by_date(hashtag='Christmas', date='2015-12-20'):
    db = MongoDb().getDB()
    lower_bound = datetime.datetime(2015, 12, 20)
    upper_bound = lower_bound + datetime.timedelta(days=7)
    cursor = db.stream.aggregate([
        {
            '$match': {
                'hashtags': hashtag,
                'time': {
                    "$gt": lower_bound,
                    "$lt": upper_bound
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'year': {'$year': '$time'},
                    'month': {'$month': '$time'},
                    'day': {'$dayOfMonth': '$time'},
                    'hour': {'$hour': "$time"}
                },
                'cnt': {'$sum': 1},
            }
        },
    ])
    res = sorted([(get_time_from_res_dict(res['_id']), res['cnt']) for res in cursor]
                 , key=lambda t: t[0])

    return {
        'dates': [t[0] for t in res],
        'cnt': [t[1] for t in res],
    }


def get_hashtags_group_by_date(hashtags, date='2015-12-20'):
    db = MongoDb().getDB()
    t = TimeCost()
    lower_bound = datetime.datetime(2015, 12, 20)
    upper_bound = lower_bound + datetime.timedelta(days=7)
    cursor = db.stream.aggregate([
        {
            '$match': {
                'hashtags': {'$in': hashtags},
                'time': {
                    '$gt': lower_bound,
                    '$lt': upper_bound
                }
            }
        },
        {'$unwind': '$hashtags'},
        {
            '$match': {
                'hashtags': {'$in': hashtags},
            }
        },
        {
            '$group': {
                '_id': {
                    'hashtags': '$hashtags',
                    'year': {'$year': '$time'},
                    'month': {'$month': '$time'},
                    'day': {'$dayOfMonth': '$time'},
                    'hour': {'$hour': "$time"}
                },
                'cnt': {'$sum': 1},
            }
        },
        {
            '$project': {
                '_id': 0,
                'hashtag': "$_id.hashtags",
                'info': {
                    'date': {
                        'year': "$_id.year",
                        'month': "$_id.month",
                        'day': "$_id.day",
                        'hour': "$_id.hour",
                    },
                    'cnt': "$cnt"
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'hashtag': '$hashtag',
                },
                'info': {'$push': '$info'}
            }
        },
    ])
    query_res = {t['_id']['hashtag']: {get_time_from_res_dict(cur['date']): cur['cnt']
                                       for cur in t['info']} for t in cursor}
    t.timecost()
    print query_res

    dates = sorted(set(x for t in query_res.values() for x in t.keys()))
    print len(dates), dates

    for key, values in query_res.items():
        for date in dates:
            if date not in values:
                values[date] = 0
        values = sorted(values.items(), key=lambda x: x[0])
        query_res[key] = [t[1] for t in values]

    return {
        "dates": dates,
        "cnt": query_res
    }


def get_hashtags_group_by_date2(hashtags, date='2015-12-20'):
    db = MongoDb().getDB()
    lower_bound = datetime.datetime(2015, 12, 20)
    upper_bound = lower_bound + datetime.timedelta(days=7)

    query_res = collections.defaultdict(dict)
    ti = TimeCost()
    for hashtag in hashtags:
        cursor = db.stream.aggregate([
            {
                '$match': {
                    'hashtags': hashtag,
                    'time': {
                        "$gt": lower_bound,
                        "$lt": upper_bound
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'year': {'$year': '$time'},
                        'month': {'$month': '$time'},
                        'day': {'$dayOfMonth': '$time'},
                        'hour': {'$hour': "$time"}
                    },
                    'cnt': {'$sum': 1},
                }
            },
        ])
        query_res[hashtag] = {get_time_from_res_dict(t['_id']): t['cnt']
                              for t in cursor}

    dates = sorted(set(x for t in query_res.values() for x in t.keys()))
    print len(dates), dates

    for key, values in query_res.items():
        for date in dates:
            if date not in values:
                values[date] = 0
        values = sorted(values.items(), key=lambda x: x[0])
        query_res[key] = [t[1] for t in values]

    ti.timecost()
    return {
        "dates": dates,
        "cnt": query_res
    }


if __name__ == '__main__':
    t = TimeCost()
    res = get_hashtag_group_by_date()
    print res['dates']
    print res['cnt']
    t.timecost()
    # res = get_hashtags_group_by_date2(hashtags=['Christmas', 'MTVStars'])
    # print res['cnt']['Christmas']
    # print res['cnt']['christmas']
    # print res['dates']
