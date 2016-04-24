# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/23.
import datetime
from sklearn.externals import joblib
import nltk
import re
import numpy as np

english_stopwords = nltk.corpus.stopwords.words('english')
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '#', '$', '%', '...']
remove_words = set(english_stopwords + english_punctuations)
wnl = nltk.WordNetLemmatizer()


# 到时候再看看 twitter_text
def _filter_tweet(tweet):
    # 替换twitter特殊字符
    tweet = re.sub(r"(RT|via)((?:\b\W*@\w+)+)", "", tweet)
    tweet = tweet.lower()
    # 替换tweet Url => URL
    tweet = re.sub(r"http[s]?://\S*", "URL", tweet)
    # 替换user mentions => @
    tweet = re.sub(r"@\w+", "@", tweet)
    tweet = ' '.join(wnl.lemmatize(word) for word in nltk.word_tokenize(tweet) if word not in remove_words)
    return tweet


def filter_tweets(original_tweets):
    return list(map(_filter_tweet, original_tweets))


class SentimentJudge(object):
    """
        Simple example:
            s = SentimentJudge()
            test_data = s.transform(_test_data)
            predicted = s.predict(test_data)
            print np.sum(predicted == _test_target), len(_test_target), np.mean(predicted == _test_target)
    """
    counter_vector = joblib.load('./classifier/counter_vector.pkl')
    classifier = joblib.load('./classifier/LogisticRegression.pkl')

    def transform(self, X):
        """
            Transform X so that to fit classifier
        :param X: [str,str...]
        :return: csr_matrix like array
        """
        return self.counter_vector.transform(filter_tweets(X))

    def predict(self, X):
        """
            Predict X is positive or negative
        :param X:
        :return: a numpy.ndarray. each row with "positive" or "negative"
        """
        return self.classifier.predict(X)


if __name__ == '__main__':
    def read_test_data():
        print 'read_test_data'
        test_data, test_target = [], []
        start = datetime.datetime.now()
        with open(r'e:\textCorpus\testdata.csv') as f:
            for i, line in enumerate(f):
                line = line.split('","')
                score, text = line[0][1:], line[-1]
                if score != '4' and score != '0':
                    continue
                try:
                    text = text[:text.rfind('"')].decode('utf-8')
                    test_data.append(text)
                    if score == '4':
                        test_target.append('positive')
                    elif score == '0':
                        test_target.append('negative')

                except Exception, e:  # print i, line, e
                    pass
        print 'read_test_data complete', datetime.datetime.now() - start
        return test_data, test_target


    def main():
        s = SentimentJudge()
        _test_data, _test_target = read_test_data()

        test_data = s.transform(_test_data)
        print type(test_data), test_data[0]
        predicted = s.predict(test_data)
        print type(predicted), predicted[0]
        print np.sum(predicted == _test_target), len(_test_target), np.mean(predicted == _test_target)


    main()
