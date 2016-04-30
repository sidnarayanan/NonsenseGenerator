#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg, twitter_samples
from Generator import TextMerger

nltk.data.path.append('/home/sid/scratch/nltk_data')
shakespeare = []
for text in ['caesar','hamlet','macbeth']:
  shakespeare += list(gutenberg.sents('shakespeare-%s.txt'%text)) 

tweets = list(twitter_samples.strings())

g = TextMerger(tweets,shakespeare)
for x in xrange(100):
  sentence,words = g(.15)
  print '\t',sentence
