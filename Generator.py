#!/usr/bin/env python3

import nltk
import numpy.random as random
from numpy import add, digitize
from math import sqrt

nltk.data.path.append('/home/sid/scratch/nltk_data')

endPunct = set(['.','!','?'])
innerPunct = set([',',';',':','-'])
allPunct = set(innerPunct); allPunct.update(endPunct)
meanLength = 10 # should get this from the corpora

DEBUG=False

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

class Phrasebook(dict):
  def __init__(self):
    super(Phrasebook,self).__init__()
  def addSentence(self,s):
    if type(s)==type(u''):
      tokens = nltk.word_tokenize(s)
    else:
     tokens = s
    nTokens = len(tokens)
    for iT in xrange(nTokens):
      t = tokens[iT]
      if not(t.isalpha()):
        continue
      phrase = tokens[iT+1:]
      if t in self:
        self[t].append(phrase)
      else:
        self[t] = [phrase]

class TextMerger(object):
  def __init__(self,corpus1,corpus2):
    # corpus1 and corpus2 are lists of sentences
    pb1 = Phrasebook()
    for s in corpus1:
      pb1.addSentence(s)
    pb2 = Phrasebook()
    for s in corpus2:
      pb2.addSentence(s)
    self.phrasebooks = [pb1,pb2]
    self.corpora = [corpus1,corpus2]
  def __call__(self,switchWeight=.1,randomizeSeed=False):
    seed=0
    if randomizeSeed: seed = random.randint(2)
    pb = self.phrasebooks[seed]
    corpus = self.corpora[seed]
    idx = random.randint(len(corpus))
    sentence = corpus[idx]
    output = []
    if type(sentence)==type(u''):
      tokens = nltk.word_tokenize(sentence)
    else:
      tokens = sentence
    output.append(tokens[0])
    iT=1
    while True:
      # print output
      if random.random_sample()<switchWeight:
        try:
          testseed = 1-seed
          phrases = self.phrasebooks[testseed][output[-1]]
          # print 'switching %i -> %i'%(seed,testseed)
          seed = testseed
          idx = random.randint(len(phrases))
          tokens = phrases[idx]
          iT=0
        except KeyError:
          pass
      if iT==len(tokens):
        break
      output.append(tokens[iT])
      iT += 1
    s = ''
    for w in output:
      if s=='' or w in allPunct or "'" in w:
        s += w
      else:
        s += ' %s'%w
    if output[-1] not in endPunct:
      s += '.'
    return s,output


class Generator(object):
  def __init__(self,corpusList,weights=[1],switchWeight=-1):
    self.corpora = []
    for i in xrange(len(corpusList)):
      improperNouns = set([])
      for x in corpusList[i]:
        if x.islower() and not(x=='i'):
          improperNouns.add(x)
      words = [parseProperNoun(x,improperNouns) for x in corpusList[i]]
      bigrams = nltk.bigrams(words)
      cfd = nltk.ConditionalFreqDist(bigrams)
      self.corpora.append(Corpus(words,cfd,weights[i]))
    self.pmf = PMF([x.weight for x in self.corpora])
    self.switchWeight = switchWeight
  def __call__(self,seed=None,mu=meanLength):
    currentState=0
    while not seed:
      iC = self.pmf()
      currentState = iC
      words = self.corpora[iC].text
      iW = random.randint(0,len(words))
      seed = words[iW]
      if not (seed.isalpha()):
        currentState=0
        seed = None
    words = []
    words.append('%s%s'%(seed[0].upper(),seed[1:]))
    nFail=0
    while len(words)<mu+sqrt(mu):
      if nFail>5:
        if DEBUG:
          print 'Continually failing on |%s|'%seed
          print 'FD is:'
          for k,v in self.corpora[self.pmf()].dist[seed].iteritems():
            print k,v
          cfd = self.corpora[self.pmf()].dist[seed]
          probdist = nltk.probability.DictionaryProbDist(cfd,False,True)
          print probdist.generate()
          print cfd.B()
          break
        nFail = 0
        if len(words)==1:
          break # hopeless
        seed = words[-2]  
        words.pop()      
      try:
        switch = (random.random_sample() > self.switchWeight)
        if switch:
          currentState = self.pmf()
        cfd = self.corpora[currentState].dist[seed]
        probdist = nltk.probability.DictionaryProbDist(cfd,False,True)
        newword = probdist.generate()
        if not(newword.isalpha() or newword in innerPunct) and newword not in endPunct:
          nFail += 1
          continue
        if newword in endPunct:
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
      if s=='' or w in allPunct:
        s += w
      else:
        s += ' %s'%w
    if words[-1] not in endPunct:
      s += '.'
    return s,words
