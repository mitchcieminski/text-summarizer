# bring in the files we need
import markov

# grab the markov matrix for the given text
textfile = open('test data/1342.txt')
(markmat , worloc) = markov.build_markov(textfile)

# call the english matrix
(engmat , engloc) = markov.build_english()

# grab the primary eigenvectors
eigentext = markov.primary_eigen(markmat , worloc)
eigeneng = markov.primary_eigen(engmat , engloc)

# compare the two
eigendiff = eigentext - eigeneng