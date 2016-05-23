# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/5.
from collections import Counter, defaultdict
import numpy as np
from Lda_text_format import filter_tweets


class Corpus(object):
    def __init__(self, tweets, min_df=10, chunk_limit=5):
        self.min_df = min_df
        self.chunk_limit = chunk_limit

        self.locations = Corpus.get_locations_info(tweets)
        self.locations_count = Counter(self.locations)

        original_docs, docs = filter_tweets([tweet['text'] for tweet in tweets])

        self.original_docs = original_docs  # list[str,str...]
        self.docs = docs  # list[list[word]] words str list
        self.vocab = Vocabulary(self.docs, min_df)
        self.to_original_id, self.doc_word, last_chunk_size = self.vocab.docs_to_bow(self.docs)
        # to_original_id： list[original_id]
        # doc_word： list[list[word_id:count]] words id list
        self.original_chunk_size = [len(self.docs)]
        self.doc_word_chunk_size = [last_chunk_size]
        self.delete_doc_word = None

    @staticmethod
    def get_locations_info(tweets):
        """
         :param tweets: twitter tweets

        "coordinates":
        {
            "coordinates":
            [
                -75.14310264,
                40.05701649
            ],
            "type":"Point"
        }

        "place":
        {
            "attributes":{},
             "bounding_box":
            {
                "coordinates":
                [[
                        [-77.119759,38.791645],
                        [-76.909393,38.791645],
                        [-76.909393,38.995548],
                        [-77.119759,38.995548]
                ]],
                "type":"Polygon"
            }
        }

        -----------

        local database:
        "geo": [
                    -75.14310264,
                    40.05701649
            ]

        """
        locations = []
        for tweet in tweets:
            cur = None
            if 'coordinates' in tweet and tweet['coordinates']:
                cur = tweet['coordinates']["coordinates"]
            elif 'place' in tweet and tweet['place']:
                try:
                    cur = tweet['place']['bounding_box']["coordinates"][0][0]
                except Exception, e:
                    print e
            elif 'geo' in tweet and tweet['geo']:
                cur = tweet['geo']
            if cur:
                cur = ",".join([str(x) for x in cur])
            locations.append(cur)
        return locations

    def update(self, tweets):
        if len(self.original_chunk_size) >= self.chunk_limit:
            self.delete_doc_word = self.doc_word[:self.doc_word_chunk_size[0]]
            print self.locations[:self.original_chunk_size[0]]

            self.locations_count = self.locations_count - Counter(self.locations[:self.original_chunk_size[0]])
            self.locations = self.locations[self.original_chunk_size[0]:]
            self.original_docs = self.original_docs[self.original_chunk_size[0]:]
            self.docs = self.docs[self.original_chunk_size[0]:]
            self.doc_word = self.doc_word[self.doc_word_chunk_size[0]:]
            self.original_chunk_size.pop(0)
            self.doc_word_chunk_size.pop(0)

        locations = Corpus.get_locations_info(tweets)
        self.locations.extend(locations)
        self.locations_count = self.locations_count + Counter(locations)

        original_docs, docs = filter_tweets([tweet['text'] for tweet in tweets])
        self.original_chunk_size.append(len(docs))
        new_word_size, delete_word_ids = self.vocab.update(docs, self.delete_doc_word)
        self.original_docs += original_docs
        self.docs += docs
        self.to_original_id, self.doc_word, last_chunk_size = self.vocab.docs_to_bow(self.docs, len(docs))
        self.doc_word_chunk_size.append(last_chunk_size)

        self.delete_doc_word = None
        print 'after update- doc:{} words:{}'.format(len(self), len(self.vocab))
        return new_word_size, delete_word_ids

    def closest_id_2_original(self, closest_tweet_id):
        return list(map(lambda x: (self.to_original_id[x[0]], x[1]), closest_tweet_id))

    def calculate_entropy(self, K, docs_topic_distribution, probability_matrix):
        '''
            To calculate entropy from given probability_matrix
        :param docs_topic_distribution: list[int]
        :param probality_matrix:  (_lambda ),size: K * V
        :return: list[entropy] for each document
        '''

        def _calculate_entropy(doc, p):
            # TODO use reduce function:
            # return reduce(lambda x: - p[x[0]] * np.log2(p[x[0]]), doc)
            return - np.sum([p[word_id] * np.log2(p[word_id]) for word_id, _ in doc])

        def _normalization(_x):
            if len(_x.shape) == 1:
                return _x * 1.0 / np.sum(_x)
            return _x * 1.0 / np.sum(_x, axis=1)[:, np.newaxis]

        print 'calculate_entropy'

        pro_matrix = _normalization(probability_matrix)
        doc_entropy = [[] for _ in xrange(K)]
        doc_entropy_id = [[] for _ in xrange(K)]
        for doc_id, (doc, topic_id) in enumerate(zip(self.doc_word, docs_topic_distribution)):
            doc_entropy[topic_id].append(_calculate_entropy(doc, pro_matrix[topic_id]))
            doc_entropy_id[topic_id].append(doc_id)

        max_entropy_id = []
        for cur_topic_entropy, cur_topic_entropy_id in zip(doc_entropy, doc_entropy_id):
            max_index = np.argmax(cur_topic_entropy)
            max_entropy_id.append((cur_topic_entropy_id[max_index], cur_topic_entropy[max_index]))
        return self.closest_id_2_original(max_entropy_id)

    def __len__(self):
        return len(self.doc_word)

    def __iter__(self):
        return iter(self.doc_word)  # [-self.chunk_size[-1]:])


class Vocabulary(object):
    def __init__(self, docs, min_df=10):
        self.min_df = min_df
        self.word_count = None
        self.id2word = None
        self.word2id = None
        self.get_word_to_id(docs)

    def get_word_to_id(self, docs):
        '''
            Get word2id and id2word for given docs.
            docs: list of list of words
        '''
        self.word_count = Counter([word for doc in docs for word in doc])
        for word, cnt in self.word_count.items():
            if cnt < self.min_df:
                del self.word_count[word]

        self.id2word = self.word_count.keys()
        self.word2id = {key: i for i, key in enumerate(self.id2word)}

    def update(self, docs, delete_docs=None):
        # docs: list of list of words
        # delete_docs : (token_id, token_count)
        if delete_docs:
            for doc in delete_docs:
                for word, cnt in doc:
                    if word in self.word_count:
                        self.word_count[word] -= cnt

        temp_wf = defaultdict(int)
        for doc in docs:
            for word in doc:
                if word in self.word_count:
                    self.word_count[word] += 1
                else:
                    temp_wf[word] += 1

        delete_words = []
        for word, cnt in self.word_count.items():
            if cnt < self.min_df:
                delete_words.append(word)
                del self.word_count[word]

        for word, cnt in temp_wf.items():
            if cnt < self.min_df:
                del temp_wf[word]

        delete_word_ids = [self.word2id[word] for word in delete_words]
        new_word_size = len(temp_wf)

        self.id2word = self.word_count.keys() + temp_wf.keys()
        self.word2id = {key: i for i, key in enumerate(self.id2word)}
        self.word_count.update(temp_wf)

        temp_wf.clear()
        return new_word_size, delete_word_ids

    def docs_to_bow(self, docs, last_original_chunk_docs_size=None):
        '''
            Convert `document` (a docs list of words list) into the bag-of-words format = list
            of `(token_id, token_count)` 2-tuples.
            return: to_original_id: list[doc_id]
                    doc_word: [[word,count]]

        '''
        if isinstance(docs, str):
            docs = [docs]

        last_chunk_size_start_id = len(docs) - last_original_chunk_docs_size if last_original_chunk_docs_size else 0
        doc_word = []
        to_original_id = []
        last_chunk_size = 0
        for doc_id, doc in enumerate(docs):
            cur_count = defaultdict(int)
            for word in doc:
                if word in self.word2id:
                    cur_count[self.word2id[word]] += 1
            if cur_count:
                doc_word.append(cur_count.items())
                to_original_id.append(doc_id)
                if doc_id >= last_chunk_size_start_id:
                    last_chunk_size += 1
        return to_original_id, doc_word, last_chunk_size

    def __len__(self):
        return len(self.word2id)
