import numpy as np
from scipy.sparse import csc_matrix, coo_matrix, dia_matrix
from scipy.sparse import linalg as la
import markov as m
from time import time

def inflate(matrix, r):
    matrix = csc_matrix(matrix, copy=True)
    matrix.data = matrix.data ** r
    m.normalize(matrix)
    return matrix

def exp(matrix, p):
    return matrix ** p

def clear_zeroes(matrix, tol):
    matrix = csc_matrix(matrix, copy=True)
    clearval = lambda (x): (x if x > tol else 0)
    clearer = np.vectorize(clearval, otypes=[np.float])
    matrix.data = clearer(matrix.data)
    matrix.eliminate_zeros()
    return matrix


def cluster(matrix, r, p, tol):
    clustify = matrix
    prevclust = None
    while prevclust is None or not prevclust.nnz == clustify.nnz:
        prevclust = clustify
        clustify = inflate(clustify,r)
        #print 'inflate!'
        clustify = clear_zeroes(clustify, tol)
        #print 'Zeroes cleared'
        clustify = exp(clustify, p)
        #print 'POW!'
    del prevclust

    clustdata = []
    clustdict = {}
    clustnum = 0

    for i in range(0, clustify.shape[0]):
        stuff = clustify.getrow(i).nonzero()[1].tolist()
        if stuff:
            clustid = clustnum
            for w in stuff:
                if clustdict.get(w, None):
                    clustid = clustdict[w]
                    break
            clustdata.extend([(w, clustid, clustify[i,w]) for w in stuff])
            if clustid == clustnum:
                clustnum += 1

    (row, col, data) = zip(*clustdata)
    clustered = coo_matrix((data, (row, col)), shape = (matrix.shape[0], clustnum))
    return m.twonorm(csc_matrix(clustered))

def lookup_cluster(transformlist):
    totaltransform = transformlist[-1]
    for transform in transformlist[-2::-1]:
        totaltransform = transform * totaltransform
    return totaltransform


def fiedler_cluster(L, k):
    L = csc_matrix(L, dtype=np.float)
    (vals, vecs) = la.eigsh(L, k + 1, sigma=0.0000000000001, which='LM')
    vecs = np.real(vecs[:,1:])
    print vals
    print vecs
    signify = lambda(x): True if x > 0 else False
    signify = np.vectorize(signify)
    vecs = signify(vecs)
    groups = {}
    for i in xrange(0, vecs.shape[0]):
        tup = tuple(vecs[i,:].tolist())
        try:
            groups[tup].append(i)
        except:
            groups[tup] = [i]
    return groups


def Laplacian(A):
    degrees = A.sum(1)
    D = dia_matrix(((degrees.transpose()),(0)), shape=A.shape)
    return D - A
