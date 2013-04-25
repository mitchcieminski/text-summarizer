# bring in the files we need
import markov
import numpy as np
from numpy import linalg as la
# prompt user for text file
#filename = raw_input('select a text file\n')
#reffile = raw_input('select a reference file\n')

filename = 'testdata/1661.txt'
refname = 'testdata/1342.txt'

# make and store the markov matrix for the given text
textfile = open(filename)
(markmat , wordloc) = markov.build_markov(textfile)

#make the reference matrix
reffile = open(refname)
(refmat , refloc) = markov.build_markov(reffile)
# call the english matrix
# (engmat , engloc) = markov.build_english()

((markmat, refmat), wordloc) = \
  markov.compare_matrices((markmat, wordloc),(refmat, refloc))


# grab the primary eigenvectors
eigentext = markov.primary_eigenvec(markmat)
eigenref = markov.primary_eigenvec(refmat)
#eigeneng = markov.primary_eigen(engmat , engloc)

# compare the two

# eigendiff = eigentext - eigenref # eng
# words = [(word, eigendiff[loc]) for (word, loc) in wordloc.iteritems()]
# words = [(word, eigentext[loc]) for (word, loc) in wordloc.iteritems()]
# words = [(word, eigenref[loc]) for (word, loc) in wordloc.iteritems()]
# print sorted(words, key = lambda s: s[1])[:-10:-1]


# percentdiff will be positive; smaller percentdiff's will indicate
# a commonly used word, whereas larger percentdiff's will indicate an
# uncommon word, likely important to the text
percentdiff = (eigentext - eigenref) / (eigentext + eigenref)
words = [(word, percentdiff[loc]) for (word, loc) in wordloc.iteritems()]
ordered =  sorted(words, key = lambda s: s[1])[:-10:-1]

for word,val in ordered:
    print "%s: %f\tsherlock:%e\tausten:%e" \
      %(word,val[0],eigentext[wordloc[word]][0],\
        eigenref[wordloc[word]][0])
