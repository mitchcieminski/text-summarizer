import markov as m
import numpy as np

(markov, wordloc) = m.build_markov(open('testdata/1342.txt'))

print 'Built'

thing = m.normalize(markov) * m.normalize(markov.transpose())

print 'normalized and multiplied'

revloc = {}
for word, index in wordloc.iteritems():
    revloc[index] = word
words = [revloc[i] for i in range(0,thing.shape[0])]
distribution = m.primary_eigenvec(m.normalize(markov)).transpose().tolist()[0]

commonness = {}
for word, likelihood in zip(words, distribution):
    commonness[word] = likelihood

intellipairs = []
stupidpairs = []
for i in range(100,110):#thing.shape[0]):
    if float(i) / 100 == i / 100:
        print '%.2f Percent' %(float(i) / thing.shape[0] * 100,)
    problist = thing.getcol(i).todense().transpose().tolist()[0]
    intelliprob = [prob / commonness[word] for prob, word in zip(problist, words)]
    coupled = sorted(zip(problist, words))[::-1]
    intellicoupled = sorted(zip(intelliprob, words))[::-1]
    intellivant, stupidrelevant = [], []
    for coupling, word in intellicoupled:
        if coupling > 10:
            intellivant.append(word)
        else:
            break
    for coupling, word in coupled:
        if coupling > 0.01:
            stupidrelevant.append(word)
        else:
            break
    intellipairs.append((words[i], intellivant))
    stupidpairs.append((words[i], stupidrelevant))

for intellipair, stupidpair in zip(intellipairs,\
                                   stupidpairs):
    print intellipair
    print stupidpair
