# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/8.

import threading
import multiprocessing
import time
from twitterDataMining.model_p.Singleton import Singleton
from twitterDataMining.model_p.twitterApi.LocalStream import LocalStream
from twitterDataMining.model_p.twitterApi.Stream import TwitterStream
from topic.models.Corpus import Corpus
from topic.models.OnlineLDA import OnlineLDA


class TopicTrendsManager(object):
    __metaclass__ = Singleton

    def __init__(self, param):
        self.param = param
        self.topics = []
        self.lock = threading.Lock()
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

        # self.topic_trends = TopicTrends(param, self.child_conn)
        # self.topic_trends.start()

        self.topic_trends = None

        topic_trends_get = threading.Thread(target=self.receive_lda_result)
        topic_trends_get.start()

    def get_result(self, param):
        """
            get LDA result
        :param param: TopicParameterManager
        :return: topic_list or None
        """
        res = None

        if not self.topic_trends:
            self.topic_trends = TopicTrends(param, self.child_conn)
            self.topic_trends.start()
            self.param = param
            return res

        if self.param == param:
            if self.lock.acquire():
                if self.topics:
                    res = self.topics.pop(0)
                self.lock.release()

        else:  # if self.param != param:
            self.param = param
            self.topic_trends.terminate()
            self.topic_trends = TopicTrends(self.param, self.child_conn)
            self.topic_trends.start()

            if self.lock.acquire():
                self.topics = []
                self.lock.release()

        return res

    def receive_lda_result(self):
        while True:
            res = self.parent_conn.recv()
            self.lock.acquire()
            self.topics.append(res)
            self.lock.release()

    def stop(self):
        if self.topic_trends:
            self.topic_trends.terminate()
            self.topic_trends = None
        self.topics = []
        # TODO stop receive_lda_result Threads


class TopicTrends(multiprocessing.Process):
    def __init__(self, param, lda_send_conn, period=60):
        super(TopicTrends, self).__init__()
        self.param = param
        self.period = period
        self.lda_send_conn = lda_send_conn
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

        self.corpus = None
        self.olda = None

    def run(self):
        if self.param.mode != 2:  # online stream data(use twitter API)
            twitter_stream = TwitterStream(self.child_conn)
            twitter_stream_thread = threading.Thread(target=twitter_stream.stream_data,
                                                     args=(self.param.track, self.param.follow, self.param.location,
                                                           self.param.storeIntoDB, self.param.storeIntoDBName,))
            twitter_stream_thread.setDaemon(True)
            twitter_stream_thread.start()

            print ' threading.active_count()', threading.active_count()
            # TODO error count > 3 kill
            while True:
                time.sleep(self.period)
                twitter_stream.ready_receive()
                tweets = self.parent_conn.recv()
                t = threading.Thread(target=self.do_some_from_data, args=(tweets,))
                t.setDaemon(True)
                t.start()

        else:  # local database data
            condition = threading.Condition()
            local_stream = LocalStream()
            local_stream_thread = threading.Thread(target=local_stream.stream_data,
                                                   args=(condition, self.param.startDate, self.param.endDate,
                                                         self.param.localCollectionsName,))
            local_stream_thread.setDaemon(True)
            local_stream_thread.start()
            print ' threading.active_count()', threading.active_count()

            if condition.acquire():
                while True:
                    print 'wait to receive'
                    if local_stream.tweets:
                        self.do_some_from_data(local_stream.tweets)
                        local_stream.tweets = []
                        condition.notify()

                    condition.wait()

    def do_some_from_data(self, tweets):
        print 'total_tweets', len(tweets)
        # DO something from tweets

        # doc_chunk = [tweet['text'] for tweet in tweets]
        print len(tweets)
        if not self.olda:
            self.corpus = Corpus(tweets, chunk_limit=self.param.LDA_timeWindow)
            self.olda = OnlineLDA(self.corpus, K=self.param.LDA_k)
        else:
            self.olda.fit(tweets)

        res = {
            "lda": self.olda.get_lda_info(),
            "geo": self.olda.corpus.locations_count,
            "hashtags": self.olda.corpus.hashtags_most_common()
        }
        print '-------lda complete'
        # for topic_id, topic_likelihood, topic_words, topic_tweets in res["lda"]:
        #     print '{}%\t{}'.format(round(topic_likelihood * 100, 2), topic_words)
        #     print '\t', topic_tweets

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
