# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/24.

import numpy as np
from sentiment.models.SentimentJudge import SentimentJudge
from twitterDataMining.model_p.twitterApi.Rest import TwitterRest


def query_sentiment_for_online_data(query_str, max_tweets=200):
    twitter_rest = TwitterRest()
    tweets = twitter_rest.search_tweets(q=query_str.encode('utf-8'), max_results=max_tweets)

    s = SentimentJudge()

    test_data = list(map(lambda x: x['text'], list(filter(lambda x: 'text' in x, tweets))))
    print 'test_data len: {} by query string: {}'.format(len(test_data), query_str)

    test_data = s.transform(test_data)

    predicted = s.predict(test_data)

    total_positive = np.sum(predicted == 'positive')
    total_tweets = test_data.shape[0]
    positive_percentage = total_positive * 1.0 / total_tweets

    print total_positive, total_tweets, positive_percentage
    return total_positive, total_tweets, positive_percentage


if __name__ == '__main__':
    while True:
        query_str = raw_input('please input the content your want to query:\n')
        print 'wait...'
        query_sentiment_for_online_data(query_str)
