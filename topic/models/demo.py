# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/7.
# just a multiprocessing and threading demo

import threading
import multiprocessing
import time


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

        print 'process count', multiprocessing.active_children()
        if self.lock.acquire():
            if self.topics:
                res = self.topics.pop(0)
            self.lock.release()
        # self.topic_trends.terminate()
        return res

    def receive_lda_result(self):
        while True:
            res = self.parent_conn.recv()
            self.lock.acquire()
            self.topics.append(res)
            # print 'receive_lda_result', res
            self.lock.release()


class TopicTrends(multiprocessing.Process):
    def __init__(self, lda_send_conn, period=2):
        super(TopicTrends, self).__init__()
        self.period = period
        self.lda_send_conn = lda_send_conn
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

    def run(self):

        twitter_stream = TwitterStream(self.child_conn)
        twitter_stream_thread = threading.Thread(target=twitter_stream.run)
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
            print 'TopicTrends threading.live : ', list(threading.enumerate())

            # print sum(tweets)
        print 'end'

    def do_some_from_data(self, data):
        # DO something from tweets
        res = sum(data)
        self.lda_send_conn.send(res)

    def terminate(self):
        super(TopicTrends, self).terminate()
        self.parent_conn.close()
        self.child_conn.close()


class TwitterStream(object):
    def __init__(self, conn):
        super(TwitterStream, self).__init__()
        self.conn = conn
        self.tweets = []
        self.get_data = False

    def run(self):
        i = 0
        while True:
            time.sleep(0.1)
            self.tweets.append(i)
            i += 1
            if self.get_data:
                self.get_data = False
                self.conn.send(self.tweets)
                self.tweets = []

    def get(self):
        self.get_data = True


def main():
    topic_trends = TopicTrendsManager()
    while True:
        res = topic_trends.get_result()
        if res:
            print res
        else:
            print 'None, wait'
        time.sleep(1)


if __name__ == '__main__':
    main()

    # time.sleep(5)
    # topic_trends.terminate()
