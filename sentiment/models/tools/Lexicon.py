# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/5/6.
import inspect
from sklearn.externals import joblib


def get_current_function_name():
    return inspect.stack()[1][3]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


neg_words = {"never", "no", "nothing", "nowhere", "none", "none", "not", "haven't", "hasn't", "hadn't", "can't",
             "couldn't", "shouldn't", "won't", "wouldn't", "don't", "didn't", "isn't", "aren't", "ain't", "n't"}

punctuation = {'.', ':', ';', '!', '?'}
specialChar = '#@%^&()_=`{}:"|[]\;\',./\n\t\r '


class Ngrams(object):
    __metaclass__ = Singleton

    def __init__(self, gram=3, min_df=5, threshold=0.6):
        self.gram = gram
        self.min_df = min_df
        self.threshold = threshold

        # self._unigram = self.load_ngram('./data/train/Semeval_unigram.txt')
        # self._bigram = self.load_ngram('./data/train/Semeval_bigram.txt')
        # self._trigram = self.load_ngram('./data/train/Semeval_trigram.txt')
        self.ngrams = [{} for _ in xrange(self.gram)]

    def create_ngram_vector(self, data, targets):
        ngram_dict = [{} for _ in xrange(self.gram)]
        encode = {
            'positive': 0,
            'negative': 1,
            'neutral': 2,
        }
        for k, words in enumerate(data):
            words = words.split()
            target = targets[k]
            words = [i.strip(specialChar).lower() for i in words]
            words = [i for i in words if i]

            for i in xrange(len(words)):
                if words[i] in neg_words:
                    for j in xrange(i + 1, len(words)):
                        if words[j] in punctuation:
                            break
                        words[j] += '_NEG'

                for gram in xrange(self.gram):
                    word = ' '.join(words[i:i + gram + 1])
                    if word not in ngram_dict[gram]:
                        ngram_dict[gram][word] = [0, 0, 0]
                    ngram_dict[gram][word][encode[target]] += 1

        for cur_gram in xrange(self.gram):
            gram_list = []
            cur_gram_dict = ngram_dict[cur_gram]
            for i in cur_gram_dict.keys():
                count = reduce(lambda x, y: x + y, cur_gram_dict[i])
                if count >= self.min_df:
                    count *= 1.0
                    pos = cur_gram_dict[i][encode['positive']] / count
                    neg = cur_gram_dict[i][encode['negative']] / count
                    neu = cur_gram_dict[i][encode['neutral']] / count
                    if pos > self.threshold or neg > self.threshold or neu > self.threshold:
                        l = [i, pos, neu, neg, count]
                        gram_list.append(l)

            gram_list = sorted(gram_list, key=lambda x: x[4], reverse=True)
            self.ngrams[cur_gram] = dict(zip([gram[0] for gram in gram_list], range(len(gram_list))))

    def get_ngram_vector(self, words):
        words = [i.strip(specialChar).lower() for i in words]
        words = [i for i in words if i]
        res = [[0 for _ in xrange(len(gram))] for gram in self.ngrams]

        for k in xrange(len(words)):
            if words[k] in neg_words:
                for j in xrange(k + 1, len(words)):
                    if words[j] in punctuation:
                        break
                    words[j] += '_NEG'

            for i, gram in enumerate(self.ngrams):
                cur_word = ' '.join(words[k: k + i + 1])
                if cur_word in gram:
                    res[i][gram[cur_word]] = 1
        ans = []
        for x in res:
            ans += x
        return ans


class Lexicon(object):
    __metaclass__ = Singleton

    def __init__(self, print_info=True):
        self.specialChar = specialChar
        self.printInfo = print_info
        self.acronymDict = self.load_acronym_dict()
        self.emoticonsDict = self.load_emotions_dict()
        self.stopWords = self.load_stop_words()
        self.intensifiers = self.load_intensifier_words()
        self.nrcUnigram, self.sen140Unigram, self.nrcUnigram_NEG, self.sen140Unigram_NEG = self.load_nrc_canada_lexicon()

        self.liubingDict = self.load_liubing_lexicon()
        self.mpqaDict = self.load_mpqa_lexicon()
        self.nrcEmotionDict = self.load_nrc_emotions_lexicon()
        self.posNegWords = self.load_pos_neg_words()
        self.afinnDict = self.load_afinn_lexicon()

    def print_load_info(self, name):
        if self.printInfo:
            print name + ' ...'

    def load_acronym_dict(self):
        # TODO 看看有没有写错
        file_path = r"./data/dictionary/acronym.txt"
        self.print_load_info(get_current_function_name())

        acronym_dict = {}
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip().split('\t')
                word = line[0].split()
                token = line[1].split()[1:]
                key = word[0].lower().strip(self.specialChar)
                value = [j.lower().strip(self.specialChar) for j in word[1:]]
                acronym_dict[key] = [value, token]
                # print filter(lambda x:x[0] != [], self.acronymDict.values())
        return acronym_dict

    def load_emotions_dict(self):
        file_path = "./data/dictionary/emoticonsWithPolarity.txt"
        self.print_load_info(get_current_function_name())
        emoticons_dict = {}
        with open(file_path) as f:
            for line in f.readlines():
                line = line.split()
                polarity = line[-1]
                emotions = line[:-1]
                for emotion in emotions:
                    emoticons_dict[emotion] = polarity
        return emoticons_dict

    def load_stop_words(self):
        # TODO 和 nltk的对比
        file_path = "./data/dictionary/stopWords.txt"
        self.print_load_info(get_current_function_name())
        stop_words = set()
        with open(file_path) as f:
            for line in f.readlines():
                word = line.strip(self.specialChar).lower()
                stop_words.add(word)
        return stop_words

    def load_intensifier_words(self):
        file_path = "./data/dictionary/intensifier.txt"
        self.print_load_info(get_current_function_name())
        intensifiers = set()
        with open(file_path) as f:
            for line in f.readlines():
                word = line.strip('\n\t').lower()
                intensifiers.add(word)
        return intensifiers

    def load_nrc_canada_lexicon(self):
        self.print_load_info(get_current_function_name())
        paths = ['./data/lexicon/NRC-Canada/NRC-Hashtag-Sentiment-Lexicon-v0.1/',
                 './data/lexicon/NRC-Canada/Sentiment140-Lexicon-v0.1/']
        types = ['unigrams-pmilexicon.txt']
        res = []
        for path in paths:
            for name in types:
                file_path = path + name
                cur_dic = {}
                with open(file_path) as f:
                    for line in f.readlines():
                        line = line.split('\t')
                        word = line[0]
                        score = float(line[1])
                        cur_dic[word] = score
                res.append(cur_dic)
        paths = [
            './data/lexicon/NRC-Canada/HashtagSentimentAffLexNegLex/HS-AFFLEX-NEGLEX-unigrams.txt',
            './data/lexicon/NRC-Canada/Sentiment140AffLexNegLex/S140-AFFLEX-NEGLEX-unigrams.txt',
        ]
        for path in paths:
            file_path = path
            cur_dic = {}
            with open(file_path) as f:
                for line in f.readlines():
                    line = line.split('\t')
                    word = line[0]
                    score = float(line[1])
                    cur_dic[word] = score
            res.append(cur_dic)

        return res

    def load_liubing_lexicon(self):
        self.print_load_info(get_current_function_name())
        path = "./data/lexicon/LiuBingLexicon/"
        file_names = [
            ("positive-words.txt", 1),
            ("negative-words.txt", -1)
        ]
        res = {}
        for file_name, score in file_names:
            file_path = path + file_name
            with open(file_path) as f:
                for line in f.readlines():
                    line = line.strip()
                    res[line] = score
        return res

    def load_mpqa_lexicon(self):
        self.print_load_info(get_current_function_name())
        file_path = "./data/lexicon/MPQALexicon/subjclueslen1-HLTEMNLP05.tff"
        res = {}
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip().split()
                _type = line[0][5:]
                word = line[2][6:]
                polarity = line[-1][14:]
                score = 1 if _type != 'strongsubj' else 2

                if polarity == 'negative':
                    score *= -1
                res[word] = score
        return res

    def load_nrc_emotions_lexicon(self):
        self.print_load_info(get_current_function_name())
        file_path = "./data/lexicon/NRC-Canada/NRC-Emotion-Lexicon-v0.92/" \
                    "NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
        res = {}
        negative_category = {'anger', 'fear', 'sadness', 'disgust', 'negative'}
        with open(file_path) as f:
            for line in f.readlines():
                word, category, flag = line.strip().split()
                if flag == '1':
                    res[word] = -1 if category in negative_category else 1
        return res

    def load_pos_neg_words(self):
        self.print_load_info(get_current_function_name())
        path = "./data/lexicon/PosNegWords/"
        file_names = [
            ("neg_mod.txt", -1),
            ("pos_mod.txt", 1)
        ]
        res = {}
        for file_name, score in file_names:
            file_path = path + file_name
            with open(file_path) as f:
                for line in f.readlines():
                    line = line.strip()
                    res[line] = score
        return res

    def load_afinn_lexicon(self):
        self.print_load_info(get_current_function_name())
        file_path = "./data/lexicon/AFINN/AFINN-111.txt"
        res = {}
        with open(file_path) as f:
            for line in f.readlines():
                line = line.strip('\n\t').split('\t')
                res[line[0]] = int(line[1])
        return res

    def cal_lexicon_feature(self, words):
        """
            词典的特征：
            人工的词典：正情感词的个数、负情感词的个数、正情感词/负情感词、
            自动生成的词典：正情感词的情感分数和、负情感词的分数和
        :return:
        """

        def cal_score_from_dic(tokens, word_score):
            max_score = last_score = pos_score_sum = neg_score_sum = pos_max = neg_max = pos_cnt = neg_cnt = 0
            for word in tokens:
                flag = 1
                if word in word_score:
                    score = flag * word_score[word]
                    if score > 0:
                        pos_score_sum += score
                        pos_cnt += 1
                        pos_max = max(pos_max, score)
                        if score > abs(max_score):
                            max_score = score
                    elif score < 0:
                        neg_score_sum += score
                        neg_cnt += 1
                        neg_max = max(neg_max, -score)
                        if -score > abs(max_score):
                            max_score = score
                    last_score = score

            # 情感词的个数
            # 总分数（正负相加）
            # 最大的分数
            # 正的分数和  负的分数和
            # 最后一个词的分数

            pos_vector = [pos_score_sum, pos_max]
            neg_vector = [neg_score_sum, -neg_max]
            vec = [pos_score_sum + neg_score_sum, pos_cnt + neg_cnt, last_score, max_score]
            return pos_vector + neg_vector + vec

        word_score_dicts = [
            self.sen140Unigram,  # 0.5918 0.5979
            self.nrcUnigram,  # 0.5666 0.5687
            self.liubingDict,  # 0.6050 0.6063
            self.mpqaDict,
            self.nrcEmotionDict,
            self.posNegWords,
            self.afinnDict,
            self.nrcUnigram_NEG,
            self.sen140Unigram_NEG,
        ]

        features = []
        for cur_word_score_dict in word_score_dicts:
            res = cal_score_from_dic(tokens=words, word_score=cur_word_score_dict)
            features.extend(res)

        return features


if __name__ == '__main__':
    pass
    # print x.acronymDict
    # print x.emoticonsDict
    # print x.stopWords
    # print x.intensifiers
    # print x.nrcUnigram
    # print x.nrcBigram
    # print x.sen140Unigram
    # print x.sen140Bigram

    # print x.liubingDict
    # print x.mpqaDict
    # print x.nrcEmotionDict
    # print x.posNegWords
