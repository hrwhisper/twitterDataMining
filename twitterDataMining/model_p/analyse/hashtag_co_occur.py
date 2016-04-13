# -*- coding:utf-8 -*-

# Created by hrwhisper on 2015/12/8.

import pymongo
import time
import datetime
import collections

if __name__ == '__main__':

    starttime = datetime.datetime.now()
    # long running

    lower_bound = str(int(time.mktime(datetime.datetime(2015, 11, 15).timetuple())) * 1000)
    upper_bound = str(int(time.mktime(datetime.datetime(2015, 11, 17).timetuple())) * 1000)
    client = pymongo.MongoClient()
    db = client.twitter
    cursor = db.stream.aggregate([
        {
            '$match': {
                'timestamp_ms': {
                    '$gt': lower_bound,
                    '$lt': upper_bound,
                },
                'entities.hashtags.0': {
                    '$exists': 'true'
                }
            }
        },
        {
            '$project': {
                'entities.hashtags': 1
            }
        }
    ]);
    cnt = 0
    hashtag_dic = collections.defaultdict(lambda: collections.defaultdict(int), {})
    for tweet in cursor:
        cnt += 1
        hashtags = tweet['entities']['hashtags']
        hashtags_len = len(hashtags)
        for i, name1 in enumerate(hashtags):
            for j, name2 in enumerate(hashtags):
                if name1 < name2:
                    hashtag_dic[name1][name2] += 1
                elif name1 > name2:
                    hashtag_dic[name2][name1] += 1
    print cnt
    res = []
    for name, dics in hashtag_dic.items():
        for name2, cnt in dics.items():
            res.append((name, name2, cnt))

    print len(res)
    hashtag_dic = sorted(res, key=lambda x: x[2], reverse=True)
    for i in hashtag_dic[:100]:
        print i

    # cursor = db.stream.find({
    #     'timestamp_ms': {
    #         '$lt': upper_bound,
    #         '$gt': lower_bound
    #     }
    # })
    # hashtag_cnt = collections.defaultdict(int)
    # for tweet in cursor:
    #     for hashtag in tweet['entities']['hashtags']:
    #         hashtag_cnt[hashtag] += 1
    # hashtag_cnt = sorted(hashtag_cnt.items(), key=lambda x: x[1], reverse=True)
    # print hashtag_cnt[:100]
    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds
