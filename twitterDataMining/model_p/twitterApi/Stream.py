# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/25.
import threading
import time
import datetime
from Basic import TwitterBasic
import twitter


class TwitterStream(TwitterBasic):
    def __init__(self, conn=None):
        TwitterBasic.__init__(self)
        # threading.Thread.__init__(self)
        self.conn = conn
        self.tweets = []
        self.get_data = False

    def ready_receive(self):
        self.get_data = True

    def stream_data(self, track_list=None, follow_list=None, geo_list=None, save_to_db=False, colname='stream'):
        """
            https://dev.twitter.com/streaming/reference/post/statuses/filter
            The default access level allows up to 400 track keywords, 5,000 follow userids and 25 0.1-360 degree location boxes.

        :param track_list:str list      ;
        :param follow_list:list (str list or int list ) ; usr_id list
        :param geo_list: list ; geo list
        :param save_to_db:
        :param colname:
        :return: None
        """
        print track_list, follow_list, geo_list, save_to_db, colname

        kwg = {'language': 'en'}

        if not track_list and not follow_list and not geo_list:
            kwg['track'] = 'twitter'

        if track_list:
            kwg['track'] = ','.join(track for track in track_list)

        if follow_list:
            kwg['follow'] = ','.join(str(follow) for follow in follow_list)

        # TODO add location list
        # if locations_list:
        #     kwg['locations'] = ','.join(str(locations) for locations in locations_list)


        twitter_stream = twitter.TwitterStream(auth=self.twitter_api.auth)
        stream = twitter_stream.statuses.filter(**kwg)
        print kwg

        for i, tweet in enumerate(stream):
            if not i % 100: print i, datetime.datetime.now(), ' ', tweet
            tweet = dict(tweet)
            if 'id' in tweet:
                self.tweets.append(tweet)

                if self.get_data:
                    self.get_data = False
                    self.conn.send(self.tweets)
                    self.tweets = []

                if save_to_db:
                    self.save_tweets_to_mongodb(tweet, colname=colname)


if __name__ == '__main__':
    def get_current_time():
        error_time = int(time.time())  # ->这是时间戳
        error_time = time.localtime(error_time)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", error_time)
        return otherStyleTime


    t = TwitterStream()
    track_list = None
    while True:
        try:
            t.stream_data(track_list=track_list, save_to_db=False, colname='stream')
        except Exception, e:
            with open('error_log.txt', 'a+') as f:
                erro_info = get_current_time() + '    ' + str(e) + ' \n'
                print erro_info
                f.write(erro_info)
