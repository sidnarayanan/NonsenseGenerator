#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg
from Generator import TextMerger
nltk.data.path.append('/home/sid/scratch/nltk_data')

with open('fearless.txt') as infile:
  s = infile.read().replace('\n',' ').decode('utf8')
  sents = nltk.sent_tokenize(s)

shakespeare = []
for text in ['sense','emma','persuasion']:
  shakespeare += list(gutenberg.sents('austen-%s.txt'%text)) 

g = TextMerger(sents,shakespeare)
for x in xrange(100):
  sentence,words = g(.15)
  print '\t',sentence
