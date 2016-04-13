# -*- coding:utf-8 -*-

# Created by hrwhisper on 2016/2/22.
# twitter text 预处理
import nltk
import re

# with open('stopwords.txt', 'r') as f:
with open('topic/models/stopwords.txt', 'r') as f:
    stopwords = [word.strip() for word in f.readlines()]

# english_stopwords = nltk.corpus.stopwords.words('english')  # + ['re', "n't"]
english_stopwords = stopwords
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '#', '$', '%', '...']
expressions = [':-)', ':)', '=)', ':D', ':-(', ':(', '=(', ';(']
remove_words = set(english_stopwords + english_punctuations + expressions)
wnl = nltk.WordNetLemmatizer()


# 到时候再看看 twitter_text
def filter_tweet(tweet):
    # 替换twitter特殊字符
    tweet = tweet.lower()
    # 替换tweet Url and user mentions
    tweet = re.sub(r"(http[s:…]*(//\S*)?)|(@\w+)", "", tweet)
    tweet = [wnl.lemmatize(word) for word in nltk.word_tokenize(tweet)]
    tweet = [word for word in tweet if word not in remove_words and len(word) >= 3]
    return tweet


def filter_tweets(original_tweets):
    _filter_tweets = list(map(filter_tweet, original_tweets))
    res_tweets = []
    res_tweets_filter = []
    for i, f_tweet in enumerate(_filter_tweets):
        if f_tweet:
            res_tweets.append(original_tweets[i])
            res_tweets_filter.append(f_tweet)
    return res_tweets, res_tweets_filter



def main():
    txt = "RT @SocialWebMining rta Mining women https://hrwhisper.me 1M+ Tweets @hrwhisper About #Syria http://wp.me/p3QiJd-1I https:…"
    print filter_tweet(txt)
    txt = "RT @StewySongs: People are people, families are families &amp; lives are lives the world over. The UK is shoulder to shoulder with Paris https:…"
    print filter_tweet(txt)

    for i, word in enumerate(english_stopwords):
        if word not in stopwords:
            print word

    print wnl.lemmatize('followed'), wnl.lemmatize('following')


if __name__ == '__main__':
    main()
