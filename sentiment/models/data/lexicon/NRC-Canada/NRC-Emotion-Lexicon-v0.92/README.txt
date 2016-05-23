
NRC Word-Emotion Association Lexicon
(NRC Emotion Lexicon)
Version 0.92
10 July 2011
Copyright (C) 2011 National Research Council Canada (NRC)
Contact: Saif Mohammad (saif.mohammad@nrc-cnrc.gc.ca)

1. This copy of the NRC Emotion Lexicon is to be used for research
purposes only.  Please contact NRC if interested in a commercial
license.

2. If you use this lexicon in your research, then please cite
at least one of the papers listed below in the PUBLICATIONS section
(preferably the journal paper in Computational Intelligence).

.......................................................................

NRC EMOTION LEXICON
-------------------
The NRC emotion lexicon is a list of words and their associations with
eight emotions (anger, fear, anticipation, trust, surprise, sadness,
joy, and disgust) and two sentiments (negative and positive). The
annotations were manually done through Amazon's Mechanical Turk. Refer
to publications below for more details.

.......................................................................

PUBLICATIONS
------------
Details of the lexicon can be found in the following peer-reviewed
publications:

-- Crowdsourcing a Word-Emotion Association Lexicon, Saif Mohammad and
Peter Turney, Computational Intelligence, 39(3), 555-590, 2013.
 	 
-- Tracking Sentiment in Mail: How Genders Differ on Emotional Axes,
Saif Mohammad and Tony Yang, In Proceedings of the ACL 2011 Workshop
on ACL 2011 Workshop on Computational Approaches to Subjectivity and
Sentiment Analysis (WASSA), June 2011, Portland, OR.  Paper (pdf)
 	 
-- From Once Upon a Time to Happily Ever After: Tracking Emotions in
Novels and Fairy Tales, Saif Mohammad, In Proceedings of the ACL 2011
Workshop on Language Technology for Cultural Heritage, Social
Sciences, and Humanities (LaTeCH), June 2011, Portland, OR.  Paper
 	 
-- Emotions Evoked by Common Words and Phrases: Using Mechanical Turk
to Create an Emotion Lexicon", Saif Mohammad and Peter Turney, In
Proceedings of the NAACL-HLT 2010 Workshop on Computational Approaches
to Analysis and Generation of Emotion in Text, June 2010, LA,
California.

Links to the papers are available here:
http://www.purl.org/net/NRCemotionlexicon
.......................................................................

VERSION INFORMATION
-------------------
Version 0.92 is the latest version as of 10 July 2011.  This version
has annotations for more than twice as many terms as in Version 0.5
which was released earlier.

.......................................................................

FORMAT
------
Each line has the following format:
TargetWord<tab>AffectCategory<tab>AssociationFlag

TargetWord is a word for which emotion associations are provided.

AffectCategory is one of eight emotions (anger, fear, anticipation,
trust, surprise, sadness, joy, or disgust) or one of two polarities
(negative or positive).

AssociationFlag has one of two possible values: 0 or 1.  0 indicates
that the target word has no association with affect category,
whereas 1 indicates an association.

.......................................................................

OTHER FORMS OF THE LEXICON
--------------------------

The original lexicon has annotations at word-sense level.  Each
word-sense pair is annotated by at least three annotators (most are
annotated by at least five).  The word-level lexicon was created by
taking the union of emotions associated with all the senses of a word.
Please contact NRC if interested in the sense-level lexicon or if
interested in more detailed information such as the individual
annotations by each of the annotators.

.......................................................................

CONTACT INFORMATION
-------------------
Saif Mohammad
Research Officer, National Research Council Canada
email: saif.mohammad@nrc-cnrc.gc.ca
phone: +1-613-993-0620

.......................................................................
