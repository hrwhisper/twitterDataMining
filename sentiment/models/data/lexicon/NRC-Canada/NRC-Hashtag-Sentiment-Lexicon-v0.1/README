NRC Hashtag Sentiment Lexicon
Version 0.1
9 April 2013
Copyright (C) 2011 National Research Council Canada (NRC)
Contact: Saif Mohammad (uvgotsaif@gmail.com)

1. This copy of the NRC Hashtag Sentiment Lexicon is to be used for research
purposes only.  Please contact NRC if interested in a commercial license.

2. If you use this lexicon in your research, then please cite
the paper listed below in the PUBLICATIONS section.

.......................................................................

NRC HASHTAG SENTIMENT LEXICON
-----------------------------
The NRC Hashtag Sentiment Lexicon is a list of words and their associations with
positive and negative sentiment. The lexicon is distributed in three files:
unigrams-pmilexicon.txt, bigrams-pmilexicon.txt, and pairs-pmilexicon.txt.

Each line in the three files has the format:

term<tab>sentimentScore<tab>numPositive<tab>numNegative
where:
   term 
      In unigrams-pmilexicon.txt, term is a unigram (single word).
	  In bigrams-pmilexicon.txt, term is a bigram (two-word sequence).
	  A bigram has the form: "string string". The bigram was seen at least once in 
	  the source tweets from which the lexicon was created. 
	  In pairs-pmilexicon.txt, term is a unigram--unigram pair,
      unigram--bigram pair, bigram--unigram pair, or a bigram--bigram pair.
	  The pairs were generated from a large set of source tweets. Tweets were examined 
	  one at a time, and all possible unigram and bigram combinations within the tweet 
	  were chosen. Pairs with certain punctuations, @ symbols, and some function words 
	  were removed.

   sentimentScore is a real number. A positive score indicates positive 
      sentiment. A negative score indicates negative sentiment. The absolute 
      value is the degree of association with the sentiment.
	  The sentiment score was calculated by subtracting the pointwise mutual
	  information (PMI) score of the term with positive hashtags and the
	  PMI of the term with negative hashtags. 
	  
	  Terms with a non-zero PMI score with positive hashtags and PMI score of 0 
	  with negative hashtags were assigned a sentimentScore of 5.
	  Terms with a non-zero PMI score with negative hashtags and PMI score of 0 
	  with positive hashtags were assigned a sentimentScore of -5.

   numPositive is the number of times the term co-occurred with a positive 
      marker such as a positive emoticon or a positive hashtag.

   numNegative is the number of times the term co-occurred with a negative 
      marker such as a negative emoticon or a negative hashtag.

The hashtag lexicon was created from a collection of tweets that had a
positive or a negative word hashtag such as #good, #excellent, #bad,
and #terrible. Version 0.1 was created from 775,310 tweets posted
between April and December 2012 using a list of 78 positive and
negative word hashtags. A list of these hashtags is shown in sentimenthashtags.txt.

The number of entries in:
  unigrams-pmilexicon.txt: 54,129 terms
  bigrams-pmilexicon.txt: 316,531 terms
  pairs-pmilexicon.txt: 308,808 terms

Refer to publication below for more details.

.......................................................................

PUBLICATION
-----------
Details of the lexicon can be found in the following peer-reviewed
publication:

-- In Proceedings of the seventh international workshop on Semantic 
Evaluation Exercises (SemEval-2013), June 2013, Atlanta, Georgia, USA. 

BibTeX entry:
@InProceedings{MohammadKZ2013,
  author    = {Mohammad, Saif and Kiritchenko, Svetlana and Zhu, Xiaodan},
  title     = {NRC-Canada: Building the State-of-the-Art in Sentiment Analysis of Tweets},
  booktitle = {Proceedings of the seventh international workshop on Semantic Evaluation Exercises (SemEval-2013)},
  month     = {June},
  year      = {2013},
  address   = {Atlanta, Georgia, USA}
}
.......................................................................

