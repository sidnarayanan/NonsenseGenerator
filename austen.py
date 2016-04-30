#!/usr/bin/env python3

import nltk
from nltk.corpus import gutenberg
from Generator import Generator

nltk.data.path.append('/home/sid/scratch/nltk_data')
words = []
split = []
for text in ['sense','emma','persuasion']:
  split.append(gutenberg.words('austen-%s.txt'%text))
  words += list(split[-1]) 
g = Generator(split,[.33,.33,1-.66],.5)
for x in xrange(10):
  while True:
    sentence,words = g('',10)
    if len(words)>1:
      print sentence
      break
