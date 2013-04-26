import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import linalg as la
import markov as m

def inflate(matrix, r):
    matrix = csc_matrix(matrix)
    matrix.data = matrix.data ** r
    return m.normalize(matrix)

def exp(matrix, p):
    return matrix ** p

def clear_zeroes(matrix, tol):
    matrix = csc_matrix(matrix)
    print len(matrix.nonzero()[0])
    for i, datum in enumerate(matrix.data):
        if datum < tol:
            matrix.data[i] = 0
    matrix.eliminate_zeros()
    print len(matrix.nonzero()[0])
    return matrix

def cluster(matrix, r, p, tol, i):
    for i in range(0, i):
        matrix = clear_zeroes(matrix, tol)
        print 'Zeroes cleared'
        matrix = exp(matrix, p)
        print 'POW!'
        matrix = inflate(matrix,r)
        print 'inflate!'
    return matrix


