# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/23.
import re
from collections import Counter
from scipy.sparse import csr_matrix
from sentiment.models.tools.Lexicon2 import Ngrams, Lexicon


def replace_emotion_pos(words, pos_tag):
    emotions_dict = Lexicon().emoticonsDict
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


def acronym_count(words):
    acronym_dict = Lexicon().acronymDict
    count = 0
    for i in xrange(len(words)):
        word = words[i].lower()
        if word in acronym_dict:
            count += 1
    return count


def remove_not_en_words(words, pos_tag):
    i = 0
    while i < len(words):
        chk = re.match(r'([a-zA-z0-9 \+\?\.\*\^\$\(\)\[\]\{\}\|\\/:;\'\"><,#@!~`%&-_=])+$', words[i])
        if chk:
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)


def remove_url(words, pos_tag):
    i = cnt = 0
    while i < len(words):
        if pos_tag[i] != 'U':
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)
            cnt += 1
    return cnt


def remove_user_mention(words, pos_tag):
    i = cnt = 0
    while i < len(words):
        if pos_tag[i] != '@' and not words[i].startswith('@'):
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)
            cnt += 1
    return cnt


def remove_preposition(words, pos_tag):
    # 介词
    i = 0
    while i < len(words):
        if pos_tag[i] != 'P':
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)


def remove_stopwords(words, pos_tag):
    i = 0
    stopword_dict = Lexicon().stopWords

    while i < len(words):
        if words[i].lower().strip(Lexicon().specialChar) not in stopword_dict:
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)


def remove_proper_common_noun(words, pos_tag):
    i = 0
    while i < len(words):
        if pos_tag[i] != '^' and pos_tag[i] != 'Z':
            i += 1
        else:
            words.pop(i)
            pos_tag.pop(i)


def replace_repeat(words):
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
            words[i] = ''.join(x).strip(Lexicon().specialChar)  # TODO remove strip?
    return count


def count_pos_tag(tokens, pos_tags):
    count = {'N': 0, 'V': 0, 'R': 0, 'O': 0, 'A': 0}
    words = {'N': [], 'V': [], 'R': [], 'O': [], 'A': []}
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(Lexicon().specialChar)
        if word:
            if pos_tags[i] in count:
                count[pos_tags[i]] += 1
                words[pos_tags[i]].append(word)
    return [count['N'], count['V'], count['R'], count['O'], count['A']], words


def find_all_capitalise(tokens, pos_tag):
    cnt = 0
    for i in range(len(tokens)):
        if pos_tag[i] != '$':
            word = tokens[i].strip(Lexicon().specialChar)
            if word:
                if word.isupper():
                    cnt += 1
    return cnt


def find_hashtags(tokens, pos_tags):
    hashtags = []
    for i in range(len(tokens)):
        if pos_tags[i] == '#':
            hashtag = tokens[i].strip(Lexicon().specialChar).lower()
            hashtags.append(hashtag)
    return hashtags


def find_negation(tokens):
    """
    takes as input a list which contains words in tokens
    and return list of words in tokens after replacement of "not","no","n't","~"
    eg isn't -> negation
    eg not -> negation
    """
    count = 0
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(Lexicon().specialChar)
        if word == "no" or word == "not" or word.count("n't") > 0:
            # tokens[i] = 'negation'
            count += 1
    return count


def find_emoticons(tokens, pos_tag):
    # TODO rename
    countEmoPos = countEmoNeg = isLastEmoPos = 0

    emoDict = Lexicon().emoticonsDict
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


def expand_negation(tokens, pos_tags):
    newTweet = []
    newToken = []
    cnt = 0
    for i in range(len(tokens)):
        word = tokens[i].lower().strip(Lexicon().specialChar)
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


def pre_process(data, pos_tags):
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

        replace_emotion_pos(data[i], pos_tags[i])
        remove_not_en_words(data[i], pos_tags[i])
        remove_url(data[i], pos_tags[i])
        remove_user_mention(data[i], pos_tags[i])

        cur_feature.append(acronym_count(data[i]))
        # replace_repeat(data[i])
        cur_feature.append(int(replace_repeat(data[i])))
        replace_hashtag_pos(data[i], pos_tags[i])

        data[i], pos_tags[i], neg_cnt = expand_negation(data[i], pos_tags[i])
        # cur_feature.append(neg_cnt)

        # remove_proper_common_noun(data[i], pos_tags[i])
        remove_preposition(data[i], pos_tags[i])

        count, words = count_pos_tag(data[i], pos_tags[i])
        cur_feature.extend(count)

        for pos in words:
            cur_feature.extend(Lexicon().cal_lexicon_feature(words[pos]))

        remove_stopwords(data[i], pos_tags[i])  # TODO 删掉一些，然后提到前面去

        cur_feature.append(find_negation(data[i]))
        cur_feature.append(find_all_capitalise(data[i], pos_tags[i]))
        cur_feature.extend(find_emoticons(data[i], pos_tags[i]))

        cur_feature.extend(Ngrams().get_ngram_vector(data[i]))

        cur_feature.extend(Lexicon().cal_lexicon_feature(find_hashtags(data[i], pos_tags[i])))

        cur_feature.extend(Lexicon().cal_lexicon_feature(data[i]))

        for feature_id, x in enumerate(cur_feature):
            if x:
                csr_feature.append(x)
                indices.append(feature_id)
        indptr.append(len(indices))

    # return features
    return csr_matrix((csr_feature, indices, indptr))


if __name__ == '__main__':
    a = [[1, 2], [3, 4, 12, 15, 3]]
    print a
    print a
