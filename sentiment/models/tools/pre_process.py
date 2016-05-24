# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/7.
import codecs
import re
from collections import Counter
import sys
import subprocess
from scipy.sparse import csr_matrix

reload(sys)
sys.setdefaultencoding('utf8')


def pos_process(data):
    # TODO use tempfile module

    temp_file_path = './t.txt'
    with codecs.open(temp_file_path, 'w+', "utf-8") as fw:
        for line in data:
            line = line.strip().split('\t')
            fw.write(line[-1].replace('\n', ' ').replace('\r', ' ') + '\n')

    cmd = ['java', '-jar', 'sentiment/models/tools/ark-tweet-nlp-0.3.2.jar', '--no-confidence', temp_file_path]
    stdin = subprocess.PIPE
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    p = subprocess.Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
    (stdout, stderr) = p.communicate()
    print stderr

    result = stdout.split('\r\n')
    tweets, pos_tags = [], []
    for i in xrange(len(result)):
        t = result[i].split('\t')
        if t and len(t) > 1:
            tweets.append(t[0])
            pos_tags.append(t[1])
    return tweets, pos_tags


def replace_emotion_pos(words, pos_tag, lexicon):
    emotions_dict = lexicon.emoticonsDict
    for i in xrange(len(words)):
        if words[i] in emotions_dict:
            # tokens[i] = emoticonsDict[tokens[i]]
            pos_tag[i] = 'E'


def replace_hashtag_pos(words, pos_tag):
    count = 0
    for i in xrange(len(words)):
        if pos_tag[i] == '#' or words[i].startswith('#'):
            count += 1
            pos_tag[i] = '#'
            # words[i] = words[i][0:].strip(Lexicon().specialChar)
    return count


def acronym_count(words, lexicon):
    acronym_dict = lexicon.acronymDict
    count = 0
    for i in xrange(len(words)):
        word = words[i].lower()
        if word in acronym_dict:
            count += 1
    return count


def remove_useless_info(words, pos_tag):
    # 删除非英文单词、URL、用户提及
    temp = zip(words, pos_tag)
    temp = filter(lambda x: re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,#@!~`%&-_=])+$', x[0]), temp)
    temp = filter(lambda x: x[1] != 'U' and x[1] != '@' and not x[0].startswith('@'), temp)
    words = [t[0] for t in temp]
    pos_tag = [t[1] for t in temp]
    return words, pos_tag


def remove_preposition(words, pos_tag):
    # 介词
    temp = zip(words, pos_tag)
    temp = filter(lambda x: x[1] != 'P', temp)
    words = [t[0] for t in temp]
    pos_tag = [t[1] for t in temp]
    return words, pos_tag


def remove_stopwords(words, pos_tag, lexicon):
    stopword_dict = lexicon.stopWords
    temp = zip(words, pos_tag)
    temp = filter(lambda x: x[0].lower().strip(lexicon.specialChar) not in stopword_dict, temp)
    words = [t[0] for t in temp]
    pos_tag = [t[1] for t in temp]
    return words, pos_tag


def replace_repeat(words, lexicon):
    """
        coooooooool -> coool
    """
    count = 0
    for i in xrange(len(words)):
        x = list(words[i])
        if len(x) > 3:
            flag = 0
            for j in xrange(3, len(x)):
                if x[j - 3].lower() == x[j - 2].lower() == x[j - 1].lower() == x[j].lower():
                    x[j - 3] = ''

                    if flag == 0:
                        count += 1
                        flag = 1
            words[i] = ''.join(x).strip(lexicon.specialChar)  # TODO remove strip?
    return count


def count_pos_tag(tokens, pos_tags, lexicon):
    count = {'N': 0, 'V': 0, 'R': 0, 'O': 0, 'A': 0}
    words = {'N': [], 'V': [], 'R': [], 'O': [], 'A': []}
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(lexicon.specialChar)
        if word:
            if pos_tags[i] in count:
                count[pos_tags[i]] += 1
                words[pos_tags[i]].append(word)
    return [count['N'], count['V'], count['R'], count['O'], count['A']], words


def find_all_capitalise(tokens, pos_tag, lexicon):
    cnt = 0
    for i in range(len(tokens)):
        if pos_tag[i] != '$':
            word = tokens[i].strip(lexicon.specialChar)
            if word:
                if word.isupper():
                    cnt += 1
    return cnt


def find_hashtags(tokens, pos_tags, lexicon):
    hashtags = []
    for i in range(len(tokens)):
        if pos_tags[i] == '#':
            hashtag = tokens[i].strip(lexicon.specialChar).lower()
            hashtags.append(hashtag)
    return hashtags


def find_negation(tokens, lexicon):
    """
    takes as input a list which contains words in tokens
    and return list of words in tokens after replacement of "not","no","n't","~"
    eg isn't -> negation
    eg not -> negation
    """
    count = 0
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(lexicon.specialChar)
        if word == "no" or word == "not" or word.count("n't") > 0:
            # tokens[i] = 'negation'
            count += 1
    return count


def find_emoticons(tokens, pos_tag, lexicon):
    # TODO rename
    countEmoPos = countEmoNeg = isLastEmoPos = 0

    emoDict = lexicon.emoticonsDict
    for i in range(len(tokens)):
        if pos_tag[i] == 'E':
            if tokens[i] in emoDict:

                emo = emoDict[tokens[i]]
                if emo == 'Extremely-Positive' or emo == 'Positive':
                    # countEmoExtremePos += 1
                    countEmoPos += 1
                    isLastEmoPos = 1
                if emo == 'Extremely-Negative' or emo == 'Negative':
                    # countEmoExtremeENeg += 1
                    countEmoNeg += 1
                    isLastEmoPos = 0

    return [
        countEmoPos,
        countEmoNeg,
        isLastEmoPos,
    ]


def expand_negation(tokens, pos_tags, lexicon):
    newTweet = []
    newToken = []
    cnt = 0
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(lexicon.specialChar)
        if word[-3:] == "n't":  # TODO 其他的否定
            cnt += 1
            if word[-5:] == "can't":
                newTweet.append('can')
            # elif word[-5:] == "won't":
            #     newTweet.append('will')
            else:
                newTweet.append(word[:-3])
            newTweet.append('not')
            newToken.append('V')
            newToken.append('R')
        else:
            newTweet.append(tokens[i])
            newToken.append(pos_tags[i])
    return newTweet, newToken, cnt


def count_marks(words):
    t = Counter(words)
    question_cnt = t.get('?', 0)
    exclamation_cnt = t.get('!', 0)
    # print question_cnt, exclamation_cnt
    return question_cnt, exclamation_cnt


def pre_process(data, pos_tags, lexicon, ngram):
    """

    :param data: [str,str]
    :param pos_tags: [pos,pos]
    :return:
    """
    indptr = [0]
    indices = []
    csr_feature = []

    for i in xrange(len(data)):
        data[i] = data[i].split()
        # TODO 直接在这里移除标点算了- -
        pos_tags[i] = pos_tags[i].split()
        cur_feature = []
        cur_feature.extend(count_marks(data[i]))

        replace_emotion_pos(data[i], pos_tags[i], lexicon)

        data[i], pos_tags[i] = remove_useless_info(data[i], pos_tags[i])

        cur_feature.append(acronym_count(data[i], lexicon))
        # replace_repeat(data[i])
        cur_feature.append(int(replace_repeat(data[i], lexicon)))
        replace_hashtag_pos(data[i], pos_tags[i])

        data[i], pos_tags[i], neg_cnt = expand_negation(data[i], pos_tags[i], lexicon)
        # cur_feature.append(neg_cnt)

        data[i], pos_tags[i] = remove_preposition(data[i], pos_tags[i])

        count, words = count_pos_tag(data[i], pos_tags[i], lexicon)
        cur_feature.extend(count)

        for pos in words:
            cur_feature.extend(lexicon.cal_lexicon_feature(words[pos]))

        data[i], pos_tags[i] = remove_stopwords(data[i], pos_tags[i], lexicon)

        cur_feature.append(find_negation(data[i], lexicon))
        cur_feature.append(find_all_capitalise(data[i], pos_tags[i], lexicon))
        cur_feature.extend(find_emoticons(data[i], pos_tags[i], lexicon))

        cur_feature.extend(ngram.get_ngram_vector(data[i]))

        cur_feature.extend(lexicon.cal_lexicon_feature(find_hashtags(data[i], pos_tags[i], lexicon)))

        cur_feature.extend(lexicon.cal_lexicon_feature(data[i]))

        for feature_id, x in enumerate(cur_feature):
            if x:
                csr_feature.append(x)
                indices.append(feature_id)
        indptr.append(len(indices))
    return csr_matrix((csr_feature, indices, indptr))


if __name__ == '__main__':
    a = [[1, 2], [3, 4, 12, 15, 3]]
    print a
    print a
