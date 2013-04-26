import markov as m
import cluster as c
import numpy as np
from scipy.sparse import csr_matrix

(markov, wordloc) = m.build_markov(open('testdata/1342.txt'))

revloc = {}
for word, index in wordloc.iteritems():
    revloc[index] = word

print 'Built'

thing = m.normalize(markov) * m.normalize(markov.transpose())
print 'normalized and multiplied'

thing = c.cluster(thing, 2, 2, 1e-3, 100)


for i in range(0, thing.shape[0]):
    stuff = thing.getrow(i).nonzero()
    if len(stuff[0]) > 5:
        print [revloc[w] for w in stuff[1].tolist()]


