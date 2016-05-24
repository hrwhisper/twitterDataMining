# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/23.
import codecs

from scipy.sparse import csr_matrix
from sklearn import metrics
from sklearn.externals import joblib
from sentiment.models.tools.pre_process import pre_process, pos_process
from sentiment.models.tools.read_data import read_all_test_data
from twitterDataMining.model_p.Singleton import Singleton


class SentimentJudge(object):
    """
        Simple example:
            s = SentimentJudge()
            test_data = s.transform(_test_data)
            predicted = s.predict(test_data)
            print np.sum(predicted == _test_target), len(_test_target), np.mean(predicted == _test_target)
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.classifier = joblib.load('sentiment/models/models_save/classifier')
        self.ngram = joblib.load('sentiment/models/models_save/ngrams')
        self.lexicon = joblib.load('sentiment/models/models_save/lexicon')

    def predict(self, X):
        """
            Predict X is positive or negative
        :param X:
        :return: a numpy.ndarray. each row with "positive" or "negative"
        """
        return self.classifier.predict(X)

    def transform(self, data, pos_tags=None):
        if pos_tags is None:
            data, pos_tags = pos_process(data)
            print len(data)
        return pre_process(data, pos_tags, self.lexicon, self.ngram)


def main():
    clf = SentimentJudge()
    tweets, target = [], []
    with codecs.open('./data/test/2014-test-journal.tsv', "r", "utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            target.append(line[1])
            tweets.append(line[2])

    test_feature = clf.transform(tweets)
    predicted = clf.predict(test_feature)
    print "Classification report for  %s:\n%s\n" % (clf,
                                                    metrics.classification_report(target, predicted, digits=3))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(target, predicted))


    # for name, test_data, test_target, test_pos in read_all_test_data():
    #     print '\n\n\n\n\n--------Now is {} --------\n\n'.format(name)
    #     test_feature = clf.transform(test_data, test_pos)
    #     predicted = clf.predict(test_feature)
    #     print "Classification report for  %s:\n%s\n" % (clf,
    #                                                     metrics.classification_report(test_target, predicted, digits=3))
    #     print("Confusion matrix:\n%s" % metrics.confusion_matrix(test_target, predicted))


if __name__ == '__main__':
    main()
