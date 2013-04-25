import numpy as np
from scipy.sparse import coo_matrix, dok_matrix, csr_matrix
from scipy.sparse import linalg as la
import re
word_re = r"[\w']+"

def normalize(matrix):
    nonzero = matrix.nonzero()
    matrix = dok_matrix(matrix)
    sums = matrix.sum(0).tolist()[0]
    (row, col, data) = zip*([(r, c, matrix[r,c] / sums[r]) if \
                             matrix[r,c] != 0 else \
                             (r, c, matrix[r,c]) for \
                             r,c in zip(nonzero[0].tolist(), \
                                        nonzero[1].tolist())])
    return coo_matrix((data, (row, col)), dtype = np.float)


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
    markmat = normalize(coo_matrix((v,(r,c)), dtype=np.float,\
                                   shape=(numwords, numwords)))

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

def write_matrix(matrix, matrix_file):
    with open(filename, 'w') as mx_file:
        for row, column, data in zip(matrix.row, matrix.col, matrix.data):
            mx_file.write('%d,%d,%f\n' % (row, column, data))

def load_matrix(filename):
    row, col, data = [],[],[]
    with open(filename) as mx_file:
        for line in mx_file.xreadlines():
            try:
                (newrow, newcol, newdata) = line.split[',']
                row.append(int(newrow))
                col.append(int(newcol))
                data.append(float(newdata))
            except:
                print 'Badly formatted line in file!'
                raise TypeError
    return coo_matrix((data,(row,col)))

def write_wordloc(wordloc, filename):
    with open(filename, 'w') as wl_file:
        for key in wordloc:
            wl_file_file.write('%s:%d\n' % (key, wordloc[key]))

def load_wordloc(filename):
    with open(filename) as wl_file:
        wordloc = {}
        for line in wl_file.xreadlines():
            line = line.split(':')
            wordloc[line[0]] = int(line[1])
    return wordloc

def process_file(filename):
    """Build and write to disk the markov matrix and its wordloc"""
    (matrix, wordloc) = build_markov(open(filename))
    prefix = filename.split['.'][0]
    write_matrix('%.mat' %prefix)
    write_wordloc('%.mat' %prefix)

def build_english():
    pass

def primary_eigenvec(matrix):
    (vec, val) = la.eigs(matrix, 1)[0]
    return vec

if __name__ == '__main__':
    files = ('testdata/1342.txt', 'testdata/1661.txt')
    for f in files:
        process_file(f)
