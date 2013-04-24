# bring in the files we need
import markov

# prompt user for text file
filename = raw_imput('select a text file\n')

# make and store the markov matrix for the given text
textfile = open(filename)
(markmat , worloc) = markov.build_markov(textfile)

# call the english matrix
(engmat , engloc) = markov.build_english()

# grab the primary eigenvectors
eigentext = markov.primary_eigen(markmat , worloc)
eigeneng = markov.primary_eigen(engmat , engloc)

# compare the two

# eigendiff will be negative; the larger the negative value, 
# the less common the word is in the whole english language
eigendiff = eigentext - eigeneng 

# percentdiff will be positive; smaller percentdiff's will indicate 
# a commonly used word, whereas larger percentdiff's will indicate an
# uncommon word, likely important to the text
percentdiff = ((eigeneng - eigentext) / ((eigeneng + eigentext)/2)) * 100