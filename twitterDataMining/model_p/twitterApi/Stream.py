# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/25.
import time
import datetime
from Basic import TwitterBasic
import twitter


class TwitterStream(TwitterBasic):
    def __init__(self, conn=None):
        TwitterBasic.__init__(self)

        self.conn = conn
        self.tweets = []
        self.get_data = False

    def ready_receive(self):
        self.get_data = True

    def stream_data(self, track=None, follow=None, locations=None, save_to_db=False,
                    collection_name='stream'):
        """
            https://dev.twitter.com/streaming/reference/post/statuses/filter
            The default access level allows up to 400 track keywords, 5,000 follow userids and 25 0.1-360 degree location boxes.

        :param track: str    ;
        :param follow:list str ;
        :param locations: str ;
        :param save_to_db:
        :param collection_name:
        :return: None
        """

        kwg = {'language': 'en'}

        if not track and not follow and not locations:
            kwg['track'] = 'twitter'

        if track:
            kwg['track'] = track

        if follow:
            kwg['follow'] = follow

        if locations:
            kwg['locations'] = locations

        twitter_stream = twitter.TwitterStream(auth=self.twitter_api.auth)
        stream = twitter_stream.statuses.filter(**kwg)
        print kwg

        for i, tweet in enumerate(stream):
            print i, datetime.datetime.now(), ' ', tweet
            tweet = dict(tweet)
            if 'id' in tweet:
                self.tweets.append(tweet)

                if self.get_data:
                    self.get_data = False
                    self.conn.send(self.tweets)
                    self.tweets = []

                if save_to_db:
                    self.save_tweets_to_mongodb(tweet, colname=collection_name)


if __name__ == '__main__':
    def get_current_time():
        error_time = int(time.time())  # ->这是时间戳
        error_time = time.localtime(error_time)
        other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", error_time)
        return other_style_time


    t = TwitterStream()
    track = None
    locations = '-122.75,36.8,-121.75,37.8,-74,40,-73,41'
    while True:
        try:
            t.stream_data(track=track, locations=locations, save_to_db=False)
        except Exception, e:
            with open('error_log.txt', 'a+') as f:
                error_info = get_current_time() + '    ' + str(e) + ' \n'
                print error_info
                f.write(error_info)
