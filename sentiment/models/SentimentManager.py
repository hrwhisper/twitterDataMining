# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/24.

import numpy as np
from sentiment.models.SentimentJudge import SentimentJudge
from twitterDataMining.model_p.twitterApi.Rest import TwitterRest


def get_result_info(predicted, target, tweets, total_tweet, return_sample_tweets_nums):
    """
    :param predicted:
    :param target:
    :param tweets: np.array  [str,str]
    :param total_tweet:
    :param return_sample_tweets_nums:
    :return:
    """
    c = predicted == target
    count = np.count_nonzero(c)
    percent = count * 1.0 / total_tweet
    c = tweets[c].tolist()
    text = sorted(c, cmp=lambda x, y: len(y) - len(x))[:return_sample_tweets_nums]
    return percent, text


def query_sentiment_for_online_data(query_str, max_tweets=200, return_sample_tweets_nums=10):
    twitter_rest = TwitterRest()
    tweets = twitter_rest.search_tweets(q=query_str.encode('utf-8'), max_results=max_tweets)
    tweets = list(set(map(lambda x: x['text'], list(filter(lambda x: 'text' in x, tweets)))))
    print 'test_data len: {} by query string: {}'.format(len(tweets), query_str)

    s = SentimentJudge()
    test_data = s.transform(tweets)
    predicted = s.predict(test_data)

    _class = ['positive', 'negative', 'neutral']
    total_tweets = test_data.shape[0]
    tweets = np.array(tweets)[:total_tweets]
    res = {}
    for target in _class:
        percent, text = get_result_info(predicted, target, tweets, total_tweets, return_sample_tweets_nums)
        res[target] = {
            'percent': percent,
            'text': text
        }
    return res
    # return total_positive, total_tweets, positive_percentage, positive_text, negative_text


if __name__ == '__main__':
    while True:
        query_str = raw_input('please input the content your want to query:\n')
        print 'wait...'
        query_sentiment_for_online_data(query_str)
