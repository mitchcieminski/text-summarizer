import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
import re
word_re = r"[\w']+"

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

    return (markmat, wordloc)

def compare_matrices( mdata0, mdata1 ):
    
    # Unpack the input
    markmats, wordlocs = (mdata0[0], mdata1[0]), (mdata0[1], mdata1[1])
    
    # Make goddamn sure it's a coo_matrix
    markmats = [coo_matrix(markmat) for markmat in markmats]
    
    # Setup the transformation
    transform = {}
    nextspot = markmats[0].shape[0]
    
    # Find what index in the second matrix corresponds to each index in
    # The first matrix and populate transform with that info
    for word in wordlocs[0]:
        try:
            transform[wordlocs[0][word]] = wordlocs[1][word]
        except KeyError:
            transform[wordlocs[0][word]] = nextspot
            wordlocs[1][word] = nextspot
            nextspot += 1
    
    # Apply the transformation
    markmats[0].row = [transform[ind] for ind in markmats[0].row]
    markmats[0].col = [transform[ind] for ind in markmats[0].col]
    
    #And add the extra rows to the second matrix
    markmats[1] = coo_matrix(markmats[1],(nextspot, nextspot))
    
    return ((markmats[0],  markmats[1]), wordlocs[1])


if __name__ == '__main__':
    files = ('1007.txt', '2007.txt')
    
    markovs = [build_markov(open(filename)) for filename in files]
    compare_matrices(markovs[0], markovs[1])
