# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/1/24.

from Basic import TwitterBasic
from functools import partial
from sys import maxint
import sys


class TwitterRest(TwitterBasic):
    def search_tweets(self, q, max_results=200, save_col_name=None, **kw):
        '''
        add since_id?
        A function to search tweets
        Twitter API use: https://dev.twitter.com/rest/reference/get/search/tweets
        Rate limit: 180 search queries per 15-minute interval.
        Notice: search index has a 7-day limit
        :param q: str   ;the content your want to query
        :param max_results: int
        :param kw: dict  ;parameter, see https://dev.twitter.com/rest/public/search
        :return: a list contains tweets
        '''
        # search_results = self.twitter_api.search.tweets(q=q, count=100, **kw)
        kw['lang'] = 'en'

        search_results = self.make_twitter_request(self.twitter_api.search.tweets, q=q, count=max_results, **kw)
        statuses = search_results['statuses']
        if save_col_name:
            self.save_tweets_to_mongodb(statuses, save_col_name)
            print statuses[0]

        # A reasonable number of results is ~1000
        # although that number of results may not exist
        # Enforce a reasonable limit
        max_results = min(1000, max_results)

        for _ in xrange(10):  # 10*100 = 1000
            try:
                next_results = search_results['search_metadata']['next_results']
            except KeyError, e:  # No more results when next_results doesn't exist
                break

            # ?max_id=690902913716133887&q=surface%20pro4&count=100&include_entities=1
            kwargs = dict([kv.split('=')
                           for kv in next_results[1:].split("&")])

            search_results = self.make_twitter_request(self.twitter_api.search.tweets, **kwargs)
            if save_col_name:
                self.save_tweets_to_mongodb(search_results['statuses'], save_col_name)
                print search_results['statuses'][0]

            statuses += search_results['statuses']
            if len(statuses) > max_results:
                break

        return statuses

    def get_user_profile(self, screen_name_list=None, user_id_list=None):
        '''
        ok
        A function get user profile by either screen_names or user_ids
        Notice: if you give both screen_name_list and user_id_list, if will query by screen_name_list
        Twitter API use: Process 100 items at a time per the API specifications for /users/lookup.
                    See https://dev.twitter.com/rest/reference/get/users/lookup for details.
        Rate limit: 180 search queries per 15-minute interval.
        :param screen_name_list: list    ; a list of screen_names
        :param user_id_list: list     ; a list of user_ids
        :return:dict  ; users profile, key is screen_name or user_id
        '''
        user_profile = {}
        label, query_list = ('screen_name', screen_name_list) if screen_name_list else ('id', user_id_list)

        while len(query_list) > 0:
            # the API limit maximum 100 user per query
            cur_query_list = ','.join([str(item) for item in query_list[:100]])
            query_list = query_list[100:]

            if screen_name_list:
                response = self.make_twitter_request(self.twitter_api.users.lookup,
                                                     screen_name=cur_query_list)
            else:  # user_ids
                response = self.make_twitter_request(self.twitter_api.users.lookup,
                                                     user_id=cur_query_list)

            user_profile.update({user_info[label]: user_info for user_info in response})

        return user_profile

    def get_friends_followers_ids(self, screen_name=None, user_id=None, friends_limit=maxint, followers_limit=maxint):
        '''
        A function get user friends or followers by either screen_name or user_id
        Notice: if you give both screen_name and user_id, if will query by screen_name
        Twitter API use: Process 5000 friends or followers at a time per the API query see
                         https://dev.twitter.com/rest/reference/get/friends/ids and
                         https://dev.twitter.com/rest/reference/get/followers/ids for details.
                         And how to use Cursor :https://dev.twitter.com/overview/api/cursoring
        Rate limit: 15 search queries per 15-minute interval.
        :param screen_name: str
        :param user_id: str
        :param friends_limit:   if 0 , not query friends
        :param followers_limit: if 0 , not query followers
        :return: two list  ; friends_ids , followers_ids
        '''

        get_friends_ids = partial(self.make_twitter_request, self.twitter_api.friends.ids,
                                  count=5000)
        get_followers_ids = partial(self.make_twitter_request, self.twitter_api.followers.ids,
                                    count=5000)

        friends_ids, followers_ids = [], []

        for twitter_api_func, limit, ids, label in [
            [get_friends_ids, friends_limit, friends_ids, "friends"],
            [get_followers_ids, followers_limit, followers_ids, "followers"]
        ]:
            if not limit:  # limit == 0
                continue

            cursor = -1
            while cursor != 0:
                if screen_name:
                    response = twitter_api_func(screen_name=screen_name, cursor=cursor)
                else:  # user_id
                    response = twitter_api_func(user_id=user_id, cursor=cursor)

                if response is not None:
                    ids += response['ids']
                    cursor = response['next_cursor']

                print >> sys.stderr, 'Fetched {0} total {1} ids for {2}'.format(len(ids),
                                                                                label, screen_name or user_id)

                # you can store data during each iteration to provide
                # an additional layer of protection from exceptional circumstances

                if len(ids) >= limit or response is None:
                    break

        # Do something useful with the IDs, like store them to disk...
        return friends_ids[:friends_limit], followers_ids[:followers_limit]

    def get_user_tweets(self, screen_name=None, user_id=None, max_results=1000):
        '''
        A function get a user tweet(3200 maximum) by either screen_name or user_id
        Notice: if you give both screen_name and user_id, if will query by screen_name.
                Traversing the timeline in Twitter's v1.1 API
                See https://dev.twitter.com/rest/public/timelines
        Twitter API use: https://dev.twitter.com/rest/reference/get/statuses/user_timeline
        Rate limit: 180 search queries per 15-minute interval.
        :param screen_name: str
        :param user_id: str
        :param max_results: int
        :return: list   ; a tweets list
        '''

        max_results, max_pages = min(max_results, 3200), 16

        kw = {
            'count': 200,
            'trim_user': 'true',
            'include_rts': 'true',
            'since_id': 1,
            'screen_name' if screen_name else 'user_id': screen_name if screen_name else user_id
        }

        tweets = self.make_twitter_request(self.twitter_api.statuses.user_timeline, **kw)
        results = tweets if tweets else []  # 401 (Not Authorized)
        print >> sys.stderr, 'Fetched %i tweets' % len(tweets)

        page_num = 1

        # Save precious request:
        # 1. the max_results < 200  after the first query
        # 2. max_result is 400, but you get 87 tweets during second query. Don't make a third request
        # Notice: Don't strictly check for the number of results being 200. You might get
        # back 198, for example, and still have many more tweets to go. you can have the
        # total number of tweets for an account (by GET /users/lookup/) as a guide.

        if kw['count'] < max_results:
            while page_num < max_pages and tweets and len(tweets) > 190 and len(results) < max_results:
                kw['max_id'] = min([tweet['id'] for tweet in tweets]) - 1

                tweets = self.make_twitter_request(self.twitter_api.statuses.user_timeline, **kw)
                results += tweets
                print >> sys.stderr, 'Fetched %i tweets' % (len(tweets),)

                page_num += 1

        print >> sys.stderr, 'Done fetching tweets'
        return results[:max_results]

    def get_remain_info(self):
        search_results = self.make_twitter_request(self.twitter_api.application.rate_limit_status)
        print search_results


if __name__ == '__main__':
    twitterRest = TwitterRest()
    # users = twitterRest.get_user_profile(screen_name_list=[ 'GabeAul', 'FCBarcelona'])
    # users = twitterRest.get_user_tweets(screen_name='hrwhisper_test',max_results=200)
    # for user in users:
    #     print user
    tweets = twitterRest.search_tweets(q="Oscars".encode('utf-8'), max_results=10000, save_col_name='Oscars')
    print len(tweets)
