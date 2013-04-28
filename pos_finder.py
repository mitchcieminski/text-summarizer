import markov as m
import cluster as c
import numpy as np
from scipy.sparse import csr_matrix
from time import time
(markov, wordloc) = m.build_markov(open('testdata/1342.txt'))
#(markov, wordloc) = m.build_markov(open('markov.py'))
#(markov, wordloc) = m.load_reference()

revloc = {}
for word, index in wordloc.iteritems():
    revloc[index] = word

print 'Built'

thing = m.normalize(markov) * m.normalize(markov.transpose())

print 'normalized and multiplied'

#start = time()
thing = c.clear_zeroes(m.normalize(markov) * m.normalize(markov.transpose()), 1e-3)
#print 'zeroes cleared: %fs' %(time()-start,)
# clustered = [thing]
# transform = []
# print thing.shape
# for i in xrange(1, 5):
#     transform.append(c.cluster(clustered[-1], 1.2, 2, 1e-3))
#     clustered.append(transform[-1].transpose() * clustered[-1] * transform[-1])
#     print clustered[-1].shape

# lookup = c.lookup_cluster(transform)

# print lookup.shape

# for i in xrange(0,lookup.shape[0]):
#     stuff = lookup.getcol(i).nonzero()[0].tolist()
#     if len(stuff) >= 5:
#         words = [revloc[w] for w in stuff]
#         print words

svd_clustered = c.svd_cluster(thing, 10, 0.001)
for i in xrange(0,svd_clustered[0].shape[1]):
    stuff = svd_clustered[0][:,i].nonzero()[0].tolist()
    if len(stuff) > 5:
        print [revloc[w] for w in stuff]
