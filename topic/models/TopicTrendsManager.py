# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/8.


import threading
import multiprocessing
import time
from twitterDataMining.model_p.twitterApi.Stream import TwitterStream
from topic.models.Corpus import Corpus
from topic.models.OnlineLDA import OnlineLDA


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TopicTrendsManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.topics = []
        self.lock = threading.Lock()
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.topic_trends = TopicTrends(self.child_conn)
        self.topic_trends.start()
        topic_trends_get = threading.Thread(target=self.receive_lda_result)
        topic_trends_get.start()

    def get_result(self):
        res = None
        if self.lock.acquire():
            if self.topics:
                res = self.topics.pop(0)
            self.lock.release()
        return res

    def receive_lda_result(self):
        while True:
            res = self.parent_conn.recv()
            self.lock.acquire()
            self.topics.append(res)
            self.lock.release()


class TopicTrends(multiprocessing.Process):
    def __init__(self, lda_send_conn, period=60):
        super(TopicTrends, self).__init__()
        self.period = period
        self.lda_send_conn = lda_send_conn
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

        self.corpus = None
        self.olda = None

    def run(self):
        twitter_stream = TwitterStream(self.child_conn)
        twitter_stream_thread = threading.Thread(target=twitter_stream.stream_data)
        twitter_stream_thread.setDaemon(True)
        twitter_stream_thread.start()

        print ' threading.active_count()', threading.active_count()
        # TODO error count > 3 kill
        while True:
            time.sleep(self.period)
            twitter_stream.get()
            tweets = self.parent_conn.recv()
            t = threading.Thread(target=self.do_some_from_data, args=(tweets,))
            t.setDaemon(True)
            t.start()
        print 'end'

    def do_some_from_data(self, tweets):
        print 'total_tweets', len(tweets)
        # DO something from tweets

        doc_chunk = [tweet['text'] for tweet in tweets]

        if not self.olda:
            self.corpus = Corpus(doc_chunk)
            self.olda = OnlineLDA(self.corpus, K=10)
        else:
            self.olda.fit(doc_chunk)

        res = self.olda.get_lda_info()
        for topic_id, (topic_likelihood, topic_words, topic_tweets) in res.items():
            print '{}%\t{}'.format(round(topic_likelihood * 100, 2), topic_words)
            print '\t', topic_tweets

        self.lda_send_conn.send(res)


def terminate(self):
    super(TopicTrends, self).terminate()
    self.parent_conn.close()
    self.child_conn.close()


if __name__ == '__main__':
    def main():
        topic_trends = TopicTrendsManager()
        while True:
            res = topic_trends.get_result()
            if res:
                print res
            else:
                print 'None, wait'
            time.sleep(10)


    main()
