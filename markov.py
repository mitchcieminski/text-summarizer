import numpy as np
from scipy.sparse import coo_matrix, dok_matrix, csc_matrix
from scipy.sparse import linalg as la
import re
import os
from time import time

word_re = r"[\w']+"
extext = 'testdata/1342.txt'
reference = 'testdata/reference'
pull_from = '/Users/Abe/Project_Gutenberg_Raw/'


def normalize(matrix):
    nonzero = matrix.nonzero()
    sums = matrix.sum(0)
    matrix = csc_matrix(matrix)

    for i in xrange(matrix.shape[1]):
        col_vals = matrix.data[matrix.indptr[i]:matrix.indptr[i + 1]].copy()
        matrix.data[matrix.indptr[i]:matrix.indptr[i + 1]] = col_vals / np.sum(col_vals)

    return matrix

def twonorm(matrix):
    nonzero = matrix.nonzero()
    sums = matrix.sum(0)
    matrix = csc_matrix(matrix)
    
    for i in xrange(matrix.shape[1]):
        col_vals = matrix.data[matrix.indptr[i]:matrix.indptr[i + 1]].copy()
        matrix.data[matrix.indptr[i]:matrix.indptr[i + 1]] = \
                                            col_vals / np.sum(np.square(col_vals))

    return matrix    


def build_markov(textfile):

    r,c,v = [],[],[]# The building blocks of the matrix
    wordloc = {}
    numwords = 0

    for line in textfile.xreadlines():
        line = re.findall(word_re, line.lower())
        for words in zip(line[:-1], line[1:]):
            indices = []
            for word in words:
                ind = wordloc.get(word, -1)
                if ind == -1:
                    ind = numwords
                    wordloc[word] = ind
                    numwords += 1
                indices.append(ind)
            c.append(indices[0])
            r.append(indices[1])
            v.append(1)

    markmat = csc_matrix(coo_matrix((v,(r,c)), dtype=np.float, shape=(numwords, numwords)))
    return (markmat, wordloc)

def compare_matrices( mdata0, mdata1 ):
    
    #Check for the edge case:
    if not mdata1:
        return ((mdata0[0], coo_matrix(mdata0[0].shape)), mdata0[1])

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

def write_data(data, filename):
    """Writes all the data about a text string to a single file, in
    the format: number of words in the test string, followed by the
    dictionary mapping words to indexes, followed by the matrix"""
    (matrix, wordloc) = data
    matrix = coo_matrix(matrix)
    with open(filename, 'w') as data_file:
        for key in wordloc:
            data_file.write('%s:%d\n' % (key, wordloc[key]))
        data_file.write('MATRIX\n')
        for row, column, data in zip(matrix.row, matrix.col, matrix.data):
            data_file.write('%d,%d,%f\n' % (row, column, data))

def load_data(filename):
    wordloc = {}
    row, col, data = [],[],[]
    with open(filename) as data_file:
        for line in data_file.xreadlines():
            try:
                line = line.split(':')
                wordloc[line[0]] = int(line[1])
            except:
                break;
        for line in data_file.xreadlines():
            try:
                (newrow, newcol, newdata) = line.split(',')
                row.append(int(newrow))
                col.append(int(newcol))
                data.append(float(newdata))
            except:
                print 'Bady Formatted Line: %s' %line
                raise TypeError

    return (csc_matrix(coo_matrix((data,(row,col)))), wordloc)

def process_file(filename):
    """Build and write to disk the markov matrix and its wordloc"""
    with open(filename) as textfile:
        try:
            data = build_markov(textfile)
        except ValueError:
            print 'INVALID FILE'
            return
    prefix = filename.split('.')[0]
    write_data(data, '%s.mark' %prefix)


def process_reference():
    start = time()
    prev = start
    for i, filename in enumerate(os.listdir(pull_from)):
        if filename.split('.')[-1] == 'txt':
            process_file(os.path.join(pull_from, filename))
        now = time()
        if float(i+1) / 10 == (i+1)//10:
            print 'Files %d-%d took %fs of %fs total, an average of %fs/file overall.\n'\
            %(i-9,i+1, now - prev, now - start, (now - start) / (10 * (i+1)))
            prev = now

def build_reference(ref=None):
    data = (load_data(os.path.join(pull_from,filename)) for \
            filename in os.listdir(pull_from) if \
            filename.split('.')[-1] == 'mark')
    ref = None
    for i, datum in enumerate(data):
        ((md, mr),wl) = compare_matrices(datum, ref)
        ref = (mr +  md, wl)
        if float(i+1) / 10 == (i+1) // 10:
            write_data(ref, reference + '.mark') 
            print 'written'


def load_reference():
    (matrix, wordloc) = load_data(reference + '.mark')
    return (matrix, wordloc)

def primary_eigenvec(matrix):
    (val, vec) = la.eigs(matrix, 1)
    vec = np.absolute(vec / vec.sum())
    return vec

if __name__ == '__main__':
    #files = ('testdata/1342.txt', 'testdata/1661.txt')
    start = time()
    #data = []
    #for i, f in enumerate(files):
    #    process_file(f)
    #process_reference()
    build_reference()
    #print load_reference()
    print time() - start
