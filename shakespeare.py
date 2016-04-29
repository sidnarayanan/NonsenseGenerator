#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg
from Generator import Generator

nltk.data.path.append('/home/sid/scratch/nltk_data')
words = []
for text in ['caesar','hamlet','macbeth']:
  words += list(gutenberg.words('shakespeare-%s.txt'%text)) 
g = Generator([words])
for x in xrange(10):
  sentence,words = g('',5)
  if len(words)>1:
    print sentence
