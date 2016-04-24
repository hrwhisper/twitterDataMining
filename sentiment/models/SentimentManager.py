# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/24.

import numpy as np
from sentiment.models.SentimentJudge import SentimentJudge
from twitterDataMining.model_p.twitterApi.Rest import TwitterRest


def query_sentiment_for_online_data(query_str, max_tweets=200, return_sample_tweets_nums=10):
    twitter_rest = TwitterRest()
    tweets = twitter_rest.search_tweets(q=query_str.encode('utf-8'), max_results=max_tweets)

    s = SentimentJudge()

    tweets = list(map(lambda x: x['text'], list(filter(lambda x: 'text' in x, tweets))))
    print 'test_data len: {} by query string: {}'.format(len(tweets), query_str)

    test_data = s.transform(tweets)

    predicted = s.predict(test_data)
    positive_predict = predicted == 'positive'
    negative_predict = predicted == 'negative'

    total_positive = np.count_nonzero(positive_predict)
    total_tweets = test_data.shape[0]
    positive_percentage = total_positive * 1.0 / total_tweets

    print total_positive, total_tweets, positive_percentage

    tweets = np.array(tweets)
    positive_predict = set(tweets[positive_predict].tolist())
    negative_predict = set(tweets[negative_predict].tolist())

    positive_text = sorted(positive_predict, cmp=lambda x, y: len(y) - len(x))[:return_sample_tweets_nums]
    negative_text = sorted(negative_predict, cmp=lambda x, y: len(y) - len(x))[:return_sample_tweets_nums]

    # pprint(positive_predict)
    # pprint(negative_predict)

    return total_positive, total_tweets, positive_percentage, positive_text, negative_text

if __name__ == '__main__':
    while True:
        query_str = raw_input('please input the content your want to query:\n')
        print 'wait...'
        query_sentiment_for_online_data(query_str)
