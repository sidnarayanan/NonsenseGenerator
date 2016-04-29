#!/usr/bin/env python3

import nltk
import numpy.random as random
from numpy import add, digitize
from math import sqrt

endPunctuation = set(['.','!','?'])
innerPunctuation = set([',',';',':','-'])
allPunctuation = set(innerPunctuation); allPunctuation.update(endPunctuation)
meanLength = 10 # should get this from the corpora

def parseProperNoun(word,nounSet):
  if word=='i':                return 'I' # hack
  if word.islower():           return word
  if word.lower() in nounSet:  return word.lower()
  return word

class PMF(object):
  def __init__(self,probabilities):
    self.bins = add.accumulate(probabilities)
  def __call__(self):
    return digitize(random.random_sample(),self.bins)

class Corpus(object):
  def __init__(self,text,dist,weight):
    self.text = text
    self.dist = dist
    self.weight = weight

class Generator(object):
  def __init__(self,corpusList,weights=[1]):
    self.corpora = []
    for i in xrange(len(corpusList)):
      improperNouns = set([])
      for x in corpusList[i]:
        if x.islower() and not(x=='i'):
          improperNouns.add(x)
      words = [parseProperNoun(x,improperNouns) for x in corpusList[i]]
      # for x in corpusList[i]:
      #   if x.islower():
      #     words.append
      #   if x.lower() in improperNouns:
      #     words.append(x.lower())
      #   else:
      #     words.append(x)
      # words = corpusList[i]
      # words = [x.lower() for x in corpusList[i]]
      bigrams = nltk.bigrams(words)
      cfd = nltk.ConditionalFreqDist(bigrams)
      self.corpora.append(Corpus(words,cfd,weights[i]))
    self.pmf = PMF([x.weight for x in self.corpora])
  def __call__(self,seed=None,mu=meanLength):
    while not seed:
      iC = self.pmf()
      words = self.corpora[iC].text
      iW = random.randint(0,len(words))
      seed = words[iW]
      if not (seed.isalpha()):
        seed = None
    words = []
    words.append('%s%s'%(seed[0].upper(),seed[1:]))
    nFail=0
    while len(words)<mu+sqrt(mu):
      if nFail>5:
        # print 'Continually failing on |%s|'%seed
        # print 'FD is:'
        # for k,v in self.corpora[self.pmf()].dist[seed].iteritems():
        #   print k,v
        # cfd = self.corpora[self.pmf()].dist[seed]
        # probdist = nltk.probability.DictionaryProbDist(cfd,False,True)
        # print probdist.generate()
        # print cfd.B()
        # break
        nFail = 0
        if len(words)==1:
          break # hopeless
        seed = words[-2]  
        words.pop()      
      try:
        cfd = self.corpora[self.pmf()].dist[seed]
        probdist = nltk.probability.DictionaryProbDist(cfd,False,True)
        newword = probdist.generate()
        if not(newword.isalpha() or newword in innerPunctuation) and newword not in endPunctuation:
          nFail += 1
          continue
        if newword in endPunctuation:
          if len(words)>mu-sqrt(mu) or cfd.B()==1:
            words.append(newword)
            break
          else:
            nFail += 1
            continue
        nFail = 0
        words.append(newword)
        seed = newword
      except:
        nFail += 1
        pass
    s = ''
    for w in words:
      if s=='' or w in allPunctuation:
        s += w
      else:
        s += ' %s'%w
    if words[-1] not in endPunctuation:
      s += '.'
    return s,words
