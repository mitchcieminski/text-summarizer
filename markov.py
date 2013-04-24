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
    row = [transform[ind] for ind in markmats[0].row]
    col = [transform[ind] for ind in markmats[0].col]

    #And add the extra rows to the second matrix
    markmats[0] = coo_matrix((markmats[0].data, (row,col)),\
                             (nextspot, nextspot))
    markmats[1] = coo_matrix((markmats[1].data, \
                              (markmats[1].row, markmats[1].col)),\
                              (nextspot, nextspot))

    return ((markmats[0],  markmats[1]), wordlocs[1])

def load_matrix(matrixfile):
    row, col, data = [],[],[]
    for line in matrixfile.xreadlines():
        try:
            (newrow, newcol, newdata) = line.split[',']
            row.append(int(newrow))
            col.append(int(newcol))
            data.append(float(newdata))
        except:
            print 'Badly formatted line in file!'
            raise TypeError
    return coo_matrix((data,(row,col)))

def load_wordloc(wordlocfile):
    wordloc = {}
    for line in wordlocfile.xreadlines()
        line = line.split(',')
        wordloc[line[0]] = int(line[1])
    return wordloc

def build_english():
    pass

def primary_eigenvec(matrix):
    pass

def output_markov_file(input_file, matrix_file, wordloc_file):
    #takes an input file object, builds its markov matrix, and writes to an output file object in row,col,data\newline format. Also builds the wordloc dictionary and outputs it to a word:index\newline format.

    #the output matrix files should be opened as "open(filename,'w')" so that you can write to them. I think the files have to actually exist, too.

    (matrix, wordloc) = build_markov(input_file)
    for row, column, data in zip(matrix.row, matrix.col, matrix.data):
        matrix_file.write('%d,%d,%f\n' % (row, column, data))
    matrix_file.flush()
    for key in wordloc:
        wordloc_file.write('%s:%d\n' % (key, wordloc[key]))
    matrix_file.flush()

if __name__ == '__main__':
    files = ('testdata/1342.txt', 'testdata/1661.txt')
    markovs = [build_markov(open(filename)) for filename in files]
    (newmarkovs, newwordloc) = compare_matrices(markovs[0], markovs[1])
