# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/18.
import datetime
from Basic import MongoDb
from topic.models.OnlineLDA import chunkize_serial


class LocalStream(object):
    def __init__(self):
        self.db = MongoDb().get_db()
        self.tweets = []

    def stream_data(self, condition, start_date, end_date, collection_name='stream'):
        cursor = self.db[collection_name].find(
            # [{
            #     '$match': {
            #         'date': {
            #             '$gt': datetime.datetime.strptime(start_date, '%Y-%m-%d'),
            #             '$lt': datetime.datetime.strptime(end_date, '%Y-%m-%d')
            #         }
            #     }},
            # {'$sort': {'date': 1}},
            # {'$project': {'text': 1, 'date': 1}},]
        )

        if condition.acquire():
            print 'loading local data'
            for doc_chunk in chunkize_serial(cursor, 3000, as_numpy=False):
                print doc_chunk[0]
                self.tweets = doc_chunk
                condition.notify()
                condition.wait()


if __name__ == '__main__':
    def main():
        str_date = '2015-11-13'
        t = datetime.datetime.strptime(str_date, '%Y-%m-%d')
        print t, type(t)
        print datetime.datetime(2015, 11, 13), type(datetime.datetime(2015, 11, 13))


    main()
