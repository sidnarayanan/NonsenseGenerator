#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg, twitter_samples
from Generator import TextMerger

nltk.data.path.append('/home/sid/scratch/nltk_data')

# corpus1 = []
# for text in ['sense','emma','persuasion']:
#   corpus1 += list(gutenberg.sents('austen-%s.txt'%text)) 

# corpus2 = list(gutenberg.sents('melville-moby_dick.txt'))

with open('input/joyce.txt') as infile:
  s = infile.read().replace('\n',' ').decode('utf8')
  corpus1 = nltk.sent_tokenize(s)

with open('input/wilde.txt') as infile:
  s = infile.read().replace('\n',' ').decode('utf8')
  corpus2 = nltk.sent_tokenize(s)

g = TextMerger(corpus2,corpus1)
for x in xrange(100):
  sentence,words = g(.2,True)
  print '\t',sentence
