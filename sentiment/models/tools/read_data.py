# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/3.
import codecs
import subprocess
import sys

from sentiment.models.tools.Lexicon import Ngrams


def create_pos_file(path):
    reload(sys)
    sys.setdefaultencoding('utf8')
    print 'read data from', path
    temp_file_path = '../t.txt'
    with codecs.open(path, "r", "utf-8") as f:
        with codecs.open(temp_file_path, 'w+', "utf-8") as fw:
            data = f.readlines()
            for line in data:
                line = line.strip().split('\t')
                fw.write(line[-1] + '\n')

    cmd = ['java', '-jar', './ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]
    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    (stdout, stderr) = p.communicate()

    result = stdout.split('\r\n')
    with codecs.open(path + "_pos", "w+", "utf-8") as f:
        for i, line in enumerate(data):
            line = line.strip().split('\t')
            t = result[i].split('\t')
            tweet = t[0]
            pos = t[1]
            tags = line[2]
            f.write(tags + '\t' + tweet + '\t' + pos + '\n')


def read_data(path):
    """
        return tweets_list and tags_list  for given path
    :param path: the file path eg:    c:\\a.txt
    :return: tweets_list,tags_list
    """
    print 'read data from', path

    tweets, tags, pos = [], [], []
    with codecs.open(path + '_pos', "r", "utf-8") as f:
        for line in f.readlines():
            line = line.strip().split("\t")
            tags.append(line[0])
            tweets.append(line[1])
            pos.append(line[2])
    return tweets, tags, pos


def read_train_data_by_year(year):
    train_data, train_target, pos = read_data("./data/train/" + str(year) + "-train-data.tsv")
    # train_data2, train_target2, pos2 = read_data("./data/train/" + str(year) + "-dev-data.tsv")
    # train_data = train_data + train_data2
    # train_target = train_target + train_target2
    # pos = pos + pos2
    return train_data, train_target, pos


def read_train_data(year=None):
    train_data, train_target, train_pos = [], [], []
    if year == '2013' or year is None:
        data, target, pos = read_train_data_by_year('2013')
        train_data += data
        train_target += target
        train_pos += pos

    len_2013 = len(train_pos)

    if year == '2016' or year is None:
        data, target, pos = read_train_data_by_year('2016')
        train_data += data
        train_target += target
        train_pos += pos

    Ngrams().create_ngram_vector(train_data, train_target)
    print int(len_2013 / 2.5), len(train_data[len_2013:])
    if year is None:
        len_2013_remain = int(len_2013 / 2.5)
        train_data = train_data[:len_2013_remain] + train_data[len_2013:]
        train_target = train_target[:len_2013_remain] + train_target[len_2013:]
        train_pos = train_pos[:len_2013_remain] + train_pos[len_2013:]

    return train_data, train_target, train_pos


def read_2013_test_data():
    return read_data("./data/test/2013-test-tweet.tsv")


def read_2014_test_data():
    return read_data("./data/test/2014-test-tweet.tsv")


def read_2016_test_data():
    return read_data("./data/test/2016-test-tweet.tsv")


def read_2014_sarcasm_test_data():
    return read_data("./data/test/2014-test-sarcasm.tsv")


def read_all_test_data():
    test_data_name = [
        '2013-test-tweet.tsv',
        '2013-test-sms.tsv',
        '2014-test-tweet.tsv',
        '2014-test-sarcasm.tsv',
        '2014-test-journal.tsv',
        # '2016-test-tweet.tsv'
    ]
    base_path = './data/test/'
    for name in test_data_name:
        data, target, pos = read_data(base_path + name)
        yield name, data, target, pos


def read_sentiment140_test_data():
    # test_data, test_target = [], []
    # with open(r'e:\textCorpus\testdata.csv') as f:
    #     for i, line in enumerate(f):
    #         line = line.split('","')
    #         score, text = line[0][1:], line[-1]
    #
    #         try:
    #             text = text[:text.rfind('"')]
    #             test_data.append(text)
    #             if score == '4':
    #                 test_target.append('positive')
    #             elif score == '0':
    #                 test_target.append('negative')
    #             else:
    #                 test_target.append('neutral')
    #         except Exception, e:  # print i, line, e
    #             pass
    return read_data(r'./data/test/sentiment140.testdata.tsv')


if __name__ == '__main__':
    test_data_name = ['Twitter-2013_gold.csv']
    # test_data_name = [
    #     '2013-test-tweet.tsv', '2013-test-sms.tsv',
    #     '2014-test-tweet.tsv', '2014-test-sarcasm.tsv', '2014-test-journal.tsv',
    #     '2016-test-tweet.tsv'
    # ]
    base_path = '../data/'
    for test in test_data_name:
        create_pos_file(base_path + test)

        # years = [2013, 2016]
        # base_path = '../data/train/'
        # for year in years:
        #     create_pos_file(base_path + str(year) + "-train-data.tsv")
        #     create_pos_file(base_path + str(year) + "-dev-data.tsv")

        # data, target = read_sentiment140_test_data()
        # reload(sys)
        # sys.setdefaultencoding('utf8')
        # temp_file_path = '../t.txt'
        #
        # with codecs.open(temp_file_path, 'w+', "utf-8") as fw:
        #     for line in data:
        #         fw.write(line + '\n')
        #
        # cmd = ['java', '-jar', './ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]
        # stdin = subprocess.PIPE
        # stdout = subprocess.PIPE
        # stderr = subprocess.PIPE
        # p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
        # (stdout, stderr) = p.communicate()
        #
        # result = stdout.split('\r\n')
        # with codecs.open(r"e:\textCorpus\testdata.csv_pos", "w+", "utf-8") as f:
        #     for i, line in enumerate(data):
        #         line = line.strip().split('\t')
        #         t = result[i].split('\t')
        #         tweet = t[0]
        #         pos = t[1]
        #         tags = target[i]
        #         f.write(tags + '\t' + tweet + '\t' + pos + '\n')
