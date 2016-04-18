# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/25.

import sys
import time
from urllib2 import URLError
from httplib import BadStatusLine
import datetime
import pymongo
import twitter


# TODO sigleton?
class MongoDb(object):
    def __init__(self):
        self._client = pymongo.MongoClient()
        self.db = self._client.twitter3

    def get_db(self):
        return self.db


class TwitterBasic(object):
    def __init__(self):
        self.twitter_api = self.oauth_login()
        self.db = MongoDb().get_db()

    @staticmethod
    def oauth_login():
        # XXX: Go to https://apps.twitter.com/app/new to create an app and get values
        # for these credentials that you'll need to provide in place of these
        # empty string values that are defined as placeholders.

        CONSUMER_KEY = 'gtebC0hJOZNB0GVxWG2OLi8xh'
        CONSUMER_SECRET = 'pOmlze5jjl2KZjFLiDy2KfW6mRllHVP3sd3PHEXpLeZhPARIcv'
        OAUTH_TOKEN = '4649573330-IEiLE9gFzYEc6FoBqL2zZSyYKBOn86LdkHgtvid'
        OAUTH_TOKEN_SECRET = 'a0yTvCQ612TaMw9vcHaglxUtFWM9TfnwfAS5rFDwhLOUj'

        auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                                   CONSUMER_KEY, CONSUMER_SECRET)

        twitter_api = twitter.Twitter(auth=auth)
        return twitter_api

    @staticmethod
    def make_twitter_request(twitter_api_func, max_errors=10, *args, **kw):
        # A nested helper function that handles common HTTPErrors. Return an updated
        # value for wait_period if the problem is a 500 level error. Block until the
        # rate limit is reset if it's a rate limiting issue (429 error). Returns None
        # for 401 and 404 errors, which requires special handling by the caller.
        def handle_twitter_http_error(e, wait_period=2, sleep_when_rate_limited=True):

            if wait_period > 3600:  # Seconds
                print >> sys.stderr, 'Too many retries. Quitting.'
                raise e

            # response code: https://dev.twitter.com/overview/api/response-codes

            if e.e.code == 401:
                print >> sys.stderr, 'Encountered 401 Error (Not Authorized)'
                return None
            elif e.e.code == 404:
                print >> sys.stderr, 'Encountered 404 Error (Not Found)'
                return None
            elif e.e.code == 429:
                print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)'
                if sleep_when_rate_limited:
                    print >> sys.stderr, "Retrying in 15 minutes...ZzZ..."
                    sys.stderr.flush()
                    time.sleep(60 * 15 + 5)
                    print >> sys.stderr, '...ZzZ...Awake now and trying again.'
                    return 2
                else:
                    raise e  # Caller must handle the rate limiting issue
            elif e.e.code in (500, 502, 503, 504):
                print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % \
                                     (e.e.code, wait_period)
                time.sleep(wait_period)
                wait_period *= 1.5
                return wait_period
            else:
                raise e

        wait_period = 2
        error_count = 0

        while True:
            try:
                return twitter_api_func(*args, **kw)
            except twitter.api.TwitterHTTPError, e:
                error_count = 0
                wait_period = handle_twitter_http_error(e, wait_period)
                if wait_period is None:
                    return
            except URLError, e:
                error_count += 1
                print >> sys.stderr, "URLError encountered. Continuing."
            except BadStatusLine, e:
                error_count += 1
                print >> sys.stderr, "BadStatusLine encountered. Continuing."

            if error_count > max_errors:
                print >> sys.stderr, "Too many consecutive errors...bailing out."
                raise

    def save_tweets_to_mongodb(self, tweets, colname='stream'):
        def tweets_format(original_tweet):
            tweet = {
                'id': original_tweet['id_str'],
                'text': original_tweet['text'],
                'user_id': original_tweet['user']['id_str'],
                'date': datetime.datetime.strptime(original_tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            }

            if 'coordinates' in original_tweet and original_tweet['coordinates']:
                tweet['geo'] = original_tweet['coordinates']  # original_tweet['coordinates']['coordinates']

            if original_tweet['favorite_count'] != 0:
                tweet['like'] = original_tweet['favorite_count']

            if original_tweet['in_reply_to_status_id_str']:
                tweet['reply_id'] = original_tweet['in_reply_to_status_id_str']

            if original_tweet['in_reply_to_user_id_str']:
                tweet['reply_user_id'] = original_tweet['in_reply_to_user_id_str']

            if 'quoted_status_id_str' in original_tweet:
                tweet['quoted_id'] = original_tweet['quoted_status_id_str']

            if 'quoted_status' in original_tweet:
                tweet['quoted_id'] = tweets_format(original_tweet['quoted_status'])

            if 'retweeted_status' in original_tweet:
                tweet['retweet_id'] = tweets_format(original_tweet['retweeted_status'])

            if original_tweet['retweet_count'] != 0:
                tweet['retweet_count'] = original_tweet['retweet_count']

            if original_tweet['entities']['hashtags']:
                tweet['hashtags'] = [hashtag['text'] for hashtag in original_tweet['entities']['hashtags']]

            if original_tweet['entities']['urls']:
                tweet['urls'] = [url['expanded_url'] for url in original_tweet['entities']['urls']]

            if original_tweet['entities']['user_mentions']:
                tweet['user_mentions'] = [memtion['id_str'] for memtion in original_tweet['entities']['user_mentions']]

                try:
                    DB.save(tweet)
                except Exception, e:  # dup key
                    if 'like' in tweet or 'retweet_count' in tweet:
                        t = DB.find_one({'id': tweet['id']})

                        if t:
                            change = False
                            if 'like' in tweet:
                                if 'like' not in t or ('like' in t and t['like'] < tweet['like']):
                                    t['like'] = tweet['like']
                                    change = True

                            if 'retweet_count' in tweet:
                                if 'retweet_count' not in t or (
                                                'retweet_count' in t and t['retweet_count'] < tweet['retweet_count']):
                                    t['retweet_count'] = tweet['retweet_count']
                                    change = True
                            if change:
                                DB.save(t)

                return tweet['id']

        if not isinstance(tweets, list):
            tweets = [tweets]

        DB = self.db[colname]
        for tweet in tweets:
            try:
                tweets_format(tweet)
            except Exception, e:
                print e
