import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
import re

def build_markov(textfile):

    r,c,v = [],[],[]# The building blocks of the matrix
    wordloc = {}
    numwords = 0

    for line in textfile.xreadlines():
        line = re.findall(word_re, line.lower())
        for words in zip(line[:-1], line[1:]):
            indices = [wordloc.get(words[0], -1),wordloc.get(words[1], -1)]
            for i, (ind,w) in enumerate(zip(indices, words)):
                if ind == -1:
                    wordloc[w] = numwords
                    numwords += 1
                    indices[i] = wordloc[w]
            c.append(indices[0])
            r.append(indices[1])
            v.append(1)
    markmat = coo_matrix((v,(r,c)), shape=(numwords, numwords))

    return (wordloc, markmat)

def compare_matrices( tuple0, tuple1 ):
    markmat, wordloc = (tuple0[0], tuple1[0]), (tuple0[1], tuple1[1])
    
    # Do stuff to markmat and wordloc to make the matrices the same size
    
    return ((markmat[0], wordloc[0]), (matkmat[1], wordloc[1]))
