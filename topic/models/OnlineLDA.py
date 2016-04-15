# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/4/5.
# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/3/27.
# At this update from test 17.
# Only use max entropy to calculate most representative tweet
# delete some never used function
import codecs
import datetime
from collections import Counter
import itertools
import numpy as np
import pymongo
from scipy.special import gammaln, psi
from Corpus import Corpus

np.random.seed(100000001)


def dirichlet_expectation(alpha):
    """
        For a vector theta ~ Dir(alpha), computes E[log(theta)] given alpha.
    """
    if len(alpha.shape) == 1:
        return psi(alpha) - psi(np.sum(alpha))
    return psi(alpha) - psi(np.sum(alpha, 1))[:, np.newaxis]


def chunkize_serial(iterable, chunksize, as_numpy=True):
    """
    Return elements from the iterable in `chunksize`-ed lists. The last returned
    element may be smaller (if length of collection is not divisible by `chunksize`).

    chunkize_serial(range(10), 3)
        => [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    it = iter(iterable)
    while True:
        # convert each document to a 2d numpy array (~6x faster when transmitting
        # chunk data over the wire, in Pyro)
        if as_numpy:
            wrapped_chunk = [[np.array(doc) for doc in itertools.islice(it, int(chunksize))]]
        else:
            wrapped_chunk = [list(itertools.islice(it, int(chunksize)))]
        if not wrapped_chunk[0]: break
        # memory opt: wrap the chunk and then pop(), to avoid leaving behind a dangling reference
        yield wrapped_chunk.pop()


class OnlineLDA(object):
    """
    Implements online VB for LDA as described in (Hoffman et al. 2010).
    Base on gensim and Hoffman's code.
    """

    def __init__(self, corpus, K=10, alpha=None, eta=None, tau0=1.0, kappa=0.5, iterations=50, passes=1,
                 gamma_threshold=0.001, chunk_size=3000):
        """
        Arguments:
        K: Number of topics
        vocab: A set of words to recognize. When analyzing documents, any word
           not in this set will be ignored.
        D: Total number of documents in the population. For a fixed corpus,
           this is the size of the corpus. In the truly online setting, this
           can be an estimate of the maximum number of documents that
           could ever be seen.
        alpha: Hyperparameter for prior on weight vectors theta
        eta: Hyperparameter for prior on topics beta
        tau0: A (positive) learning parameter that downweights early iterations
        kappa: Learning rate: exponential decay rate---should be between
             (0.5, 1.0] to guarantee asymptotic convergence.

        Note that if you pass the same set of D documents in every time and
        set kappa=0 this class can also be used to do batch VB.
        """
        self._corpus = corpus
        self._K = K
        self._W = len(self._corpus.vocab)
        self._D = len(corpus)
        self._alpha = 1.0 / self._K  # np.asarray([1.0 / self._K for _ in xrange(self._K)])  # 1.0 / K  #
        self._eta = 1.0 / self._K  # np.asarray([1.0 / self._K for _ in xrange(self._K)]).reshape((self._K, 1))
        self._tau0 = tau0 + 1
        self._kappa = kappa
        self._updatect = 0
        self.gamma_threshold = gamma_threshold

        # Initialize the variational distribution q(beta|lambda)
        self._lambda = 1 * np.random.gamma(100., 1. / 100., (self._K, self._W))
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = np.exp(self._Elogbeta)
        self.gamma = None

        self.iterations = iterations
        self.chunk_size = chunk_size
        self.passes = passes

        self.update()

    def inference(self, chunk):
        """
        Given a mini-batch of documents, estimates the parameters
        gamma controlling the variational distribution over the topic
        weights for each document in the mini-batch.

        Arguments:
        docs:  List of D documents. Each document must be represented
               as a string. (Word order is unimportant.) Any
               words not in the vocabulary will be ignored.

        Returns a tuple containing the estimated values of gamma,
        as well as sufficient statistics needed to update lambda.
        """
        # This is to handle the case where someone just hands us a single
        # document, not in a list.
        batchD = len(chunk)

        # Initialize the variational distribution q(theta|gamma) for
        # the mini-batch
        gamma = 1 * np.random.gamma(100., 1. / 100., (batchD, self._K))
        Elogtheta = dirichlet_expectation(gamma)
        expElogtheta = np.exp(Elogtheta)

        sstats = np.zeros(self._lambda.shape)
        # Now, for each document d update that document's gamma and phi
        for d, doc in enumerate(chunk):
            # These are mostly just shorthand (but might help cache locality)
            ids = [id for id, _ in doc]
            cts = np.array([cnt for _, cnt in doc])
            gammad = gamma[d, :]
            expElogthetad = expElogtheta[d, :]
            expElogbetad = self._expElogbeta[:, ids]  # beta : k * v
            # The optimal phi_{dwk} is proportional to
            # expElogthetad_k * expElogbetad_w. phinorm is the normalizer.
            phinorm = np.dot(expElogthetad, expElogbetad) + 1e-100  # 归一化因子，为什么选这个?
            # Iterate between gamma and phi until convergence
            for _ in xrange(self.iterations):
                lastgamma = gammad
                # We represent phi implicitly to save memory and time.
                # Substituting the value of the optimal phi back into
                # the update for gamma gives this update. Cf. Lee&Seung 2001.
                gammad = self._alpha + expElogthetad * np.dot(cts / phinorm, expElogbetad.T)
                Elogthetad = dirichlet_expectation(gammad)
                expElogthetad = np.exp(Elogthetad)
                phinorm = np.dot(expElogthetad, expElogbetad) + 1e-100
                # If gamma hasn't changed much, we're done.
                meanchange = np.mean(abs(gammad - lastgamma))
                if meanchange < self.gamma_threshold:
                    break
            gamma[d, :] = gammad
            # Contribution of document d to the expected sufficient
            # statistics for the M step.
            sstats[:, ids] += np.outer(expElogthetad.T, cts / phinorm)  # ?

            # This step finishes computing the sufficient statistics for the
            # M step, so that
            # sstats[k, w] = \sum_d n_{dw} * phi_{dwk}
            # = \sum_d n_{dw} * exp{Elogtheta_{dk} + Elogbeta_{kw}} / phinorm_{dw}.
        # 他这里先算 \sum_d n_{dw} * exp{Elogtheta_{dk}/ phinorm_{dw}. 最后 * beta 没有保存phi的结果，省内存和时间
        sstats = sstats * self._expElogbeta

        return gamma, sstats

    def do_e_step(self, chunk):
        # Do an E step to update gamma, phi | lambda for this
        # mini-batch. This also returns the information about phi that
        # we need to update lambda.
        gamma, sstats = self.inference(chunk)
        return gamma, sstats

    def do_m_step(self, chunk_len, sstats, rhot):
        # Estimate held-out likelihood for current values of lambda.
        # Update lambda based on documents.
        self._lambda = (1 - rhot) * self._lambda + rhot * (self._eta + self._D * sstats / chunk_len)
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = np.exp(self._Elogbeta)
        self._updatect += 1

    def update(self, corpus=None, print_log_perplexity=True):
        """
        First does an E step on the mini-batch given in wordids and
        wordcts, then uses the result of that E step to update the
        variational parameter matrix lambda.

        Arguments:
        docs:  List of D documents. Each document must be represented
               as a string. (Word order is unimportant.) Any
               words not in the vocabulary will be ignored.

        Returns gamma, the parameters to the variational distribution
        over the topic weights theta for the documents analyzed in this
        update.

        Also returns an estimate of the variational bound for the
        entire corpus for the OLD setting of lambda based on the
        documents passed in. This can be used as a (possibly very
        noisy) estimate of held-out likelihood.
        """

        # rhot will be between 0 and 1, and says how much to weight
        # the information we got from this mini-batch.
        if not corpus:
            corpus = self._corpus

        self.gamma = None
        for pass_ in xrange(self.passes):
            for chunk_no, chunk in enumerate(chunkize_serial(corpus, self.chunk_size)):
                rhot = pow(self._tau0 + self._updatect, -self._kappa)
                self._rhot = rhot
                gamma, sstats = self.do_e_step(chunk)
                # print 'gamma max:', gamma.max()
                self.do_m_step(len(chunk), sstats, rhot)

                if print_log_perplexity:
                    print '%d:  rho_t = %f,  held-out perplexity estimate = %.1f' % (
                        self.iterations, self._rhot, self.log_perplexity(chunk, gamma))

                if pass_ == self.passes - 1:
                    self.gamma = np.vstack((self.gamma, gamma)) if self.gamma is not None else gamma

        return self.gamma

    def fit(self, docs):
        new_word_size, delete_word_ids = self._corpus.update(docs)

        # old self._W + new_word_size - len(delete_word_ids) == new self._W
        self._W = len(self._corpus.vocab)
        self._D = len(self._corpus)
        self._updatect = 0

        # lambda update
        for id in sorted(delete_word_ids, reverse=True):
            self._lambda = np.delete(self._lambda, id, 1)

        append_lambda = 1 * np.random.gamma(100., 1. / 100., (self._K, new_word_size))
        self._lambda = np.hstack((self._lambda * 0.5, append_lambda))
        # self._lambda = 1 * np.random.gamma(100., 1. / 100., (self._K, self._W))
        self._Elogbeta = dirichlet_expectation(self._lambda)
        self._expElogbeta = np.exp(self._Elogbeta)

        # print self._W
        self.update()

    def evidence_lower_bound(self, chunk, gamma=None, subsample_ratio=1.0):
        """
        Estimates the variational bound over *all documents* using only
        the documents passed in as "docs." gamma is the set of parameters
        to the variational distribution q(theta) corresponding to the
        set of documents passed in.

        The output of this function is going to be noisy, but can be
        useful for assessing convergence.
        """

        # This is to handle the case where someone just hands us a single
        # document, not in a list.
        score = 0.0
        _lambda = self._lambda
        Elogbeta = dirichlet_expectation(_lambda)

        for d, doc in enumerate(chunk):  # stream the input doc-by-doc, in case it's too large to fit in RAM
            ids = [id for id, _ in doc]
            cts = np.array([cnt for _, cnt in doc])
            gammad = gamma[d]
            Elogthetad = dirichlet_expectation(gammad)
            phinorm = np.zeros(len(ids))
            for i in xrange(len(ids)):
                temp = Elogthetad + Elogbeta[:, ids[i]]
                tmax = max(temp)
                phinorm[i] = np.log(sum(np.exp(temp - tmax))) + tmax
            score += np.sum(cts * phinorm)
            # E[log p(doc | theta, beta)]
            # score += np.sum(cnt * logsumexp(Elogthetad + Elogbeta[:, id]) for id, cnt in doc)

            # E[log p(theta | alpha) - log q(theta | gamma)]; assumes alpha is a vector
            score += np.sum((self._alpha - gammad) * Elogthetad)
            score += np.sum(gammaln(gammad) - gammaln(self._alpha))
            score += gammaln(np.sum(self._alpha)) - gammaln(np.sum(gammad))

        # compensate likelihood for when `corpus` above is only a sample of the whole corpus
        score *= subsample_ratio

        # E[log p(beta | eta) - log q (beta | lambda)]; assumes eta is a scalar
        score += np.sum((self._eta - _lambda) * Elogbeta)
        score += np.sum(gammaln(_lambda) - gammaln(self._eta))

        if np.ndim(self._eta) == 0:
            sum_eta = self._eta * self._W
        else:
            sum_eta = np.sum(self._eta, 1)

        score += np.sum(gammaln(sum_eta) - gammaln(np.sum(_lambda, 1)))
        return score

    def log_perplexity(self, chunk, gamma=None, total_docs=None):
        """
        Calculate and return per-word likelihood bound, using the `chunk` of
        documents as evaluation corpus. Also output the calculated statistics. incl.
        perplexity=2^(-bound), to log at INFO level.

        """
        # TODO 考虑 chunk 的情况
        if total_docs is None:
            total_docs = len(chunk)
        corpus_words = sum(cnt for document in chunk for _, cnt in document)
        subsample_ratio = 1.0 * total_docs / len(chunk)
        perwordbound = self.evidence_lower_bound(chunk, gamma, subsample_ratio=subsample_ratio) / (
            subsample_ratio * corpus_words)
        return np.exp(-perwordbound)

    def get_topic_words(self, num_words=10):
        '''
            return topic words (num_words total) for each topic
        '''
        _lambda = self._lambda
        index = np.argsort(_lambda)
        res = []
        for i in xrange(self._K):
            res.append([self._corpus.vocab.id2word[word_id] for word_id in index[i][::-1][:num_words]])
        return res

    def get_doc_topic_distribution(self):
        '''
            for each document in Corpus, get their most likely topic.
            return a topic_id list
        '''
        if self.gamma is None:
            self.update()

        topic_distribution = [np.argmax(gammad) for gammad in self.gamma]
        return topic_distribution

    def get_topic_order(self, topic_distribution=None):
        '''
            return a list of tuple(topic_id,topic_probability)
        '''
        if topic_distribution is None:
            topic_distribution = self.get_doc_topic_distribution()

        topic_count = Counter(topic_distribution)
        topic_order = sorted(topic_count.items(), key=lambda x: x[1], reverse=True)
        # 兼容python 3 ,写个list
        topic_order = list(map(lambda x: (x[0], x[1] * 1.0 / self._D), topic_order))
        return topic_order

    def get_most_representative_tweets(self, topic_distribution=None):
        '''
            return a list of max entropy doc id for each document
        '''
        if topic_distribution is None:
            topic_distribution = self.get_doc_topic_distribution()
        # [(docs_id,cosine_distance)]
        distances = self._corpus.calculate_entropy(self._K, topic_distribution, self._lambda)
        # print list(map(lambda x: x[1], distances))
        min_dis_id = map(lambda x: x[0], distances)
        return min_dis_id

    def get_lda_info(self, return_topic_words=True, return_most_representative_tweets=True, order_topic=True):
        topic_order = topic_distribution = topic_words = representative_tweets = None

        if order_topic:
            topic_distribution = self.get_doc_topic_distribution()
            topic_order = self.get_topic_order(topic_distribution)
        else:
            topic_order = zip(range(self._K), [1. / self._K] * self._K)

        if return_topic_words:
            topic_words = self.get_topic_words()

        if return_most_representative_tweets:
            representative_tweets = self.get_most_representative_tweets(topic_distribution)

        res = []
        for topic_id, probability in topic_order:
            cur = [str(topic_id), probability]
            if return_topic_words:
                cur.append(topic_words[topic_id])
            if return_most_representative_tweets:
                cur.append(self._corpus.original_docs[representative_tweets[topic_id]])

            res.append(cur)
        return res


def main():
    def get_data():
        client = pymongo.MongoClient()
        db = client.twitter4
        cursor = db.stream.aggregate([
            {'$match': {
                'date': {
                    '$gt': datetime.datetime(2015, 11, 13)
                }
            }},
            {'$sort': {'date': 1}},
            {'$project': {'text': 1, 'date': 1}},
        ])
        return cursor

    def get_remote_data():
        client = pymongo.MongoClient(host='59.77.134.176')
        db = client.twitter3
        cursor = db.stream.aggregate([
            # {'$sort': {'date': 1}},
            {'$project': {'text': 1}},
        ])
        return cursor

    cursor = get_data()
    print 'calculate_entropy 多个词只算1次'
    olda = None
    reallen = 0
    # for chunk_no, doc_chunk in enumerate(cursor_serial(cursor, 3000)):
    for chunk_no, doc_chunk in enumerate(chunkize_serial(cursor, 3000, as_numpy=False)):
        print doc_chunk[0]['date']
        doc_chunk = [tweet['text'] for tweet in doc_chunk]

        reallen += len(doc_chunk)

        print chunk_no, reallen - len(doc_chunk), reallen, len(doc_chunk), 'lda'
        start = datetime.datetime.now()
        if not olda:
            corpus = Corpus(doc_chunk)
            olda = OnlineLDA(corpus, K=10)
        else:
            olda.fit(doc_chunk)
        # Give them to online LDA

        print datetime.datetime.now() - start
        with codecs.open(r'G:\test18.out', "w", "utf-8-sig") as f:
            for topic_id, (topic_likelihood, topic_words, topic_tweets) in olda.get_lda_info():
                print '{}%\t{}'.format(round(topic_likelihood * 100, 2), topic_words)
                print '\t', topic_tweets
                f.write(topic_tweets + '\n')

        print '\n\n\n\n\n\n'


if __name__ == '__main__':
    main()
