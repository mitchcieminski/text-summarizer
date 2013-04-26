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
pairs = []

for i in range(0,thing.shape[0]):
    problist = thing.getcol(i).todense().transpose().tolist()[0]
    coupled = zip(*sorted(zip(problist, words)))
    pairs.append((words[i], coupled[1][-4:]))

for pair in pairs[100:110]:
    print pair
