#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg
from Generator import TextMerger
nltk.data.path.append('/home/sid/scratch/nltk_data')

with open('fearless.txt') as infile:
  s = infile.read().replace('\n',' ').decode('utf8')
  sents = nltk.sent_tokenize(s)

g = TextMerger(sents,sents)
for x in xrange(100):
  sentence,words = g(.5)
  print '\t',sentence
