import numpy as np
from numpy import linalg


"""
Effective resistance

Harry Richman 2024
"""

def laplacian_matrix(A):
    Q = np.array(A)
    n = len(A)
    for i in range(n):
        # set diagonal entry
        Q[i, i] = sum(A[i])
        for j in range(i):
            # set off-diagonal entries
            Q[i, j] = Q[j, i] = - A[i][j]
    return Q

def unit_vec(i, n):
    e = np.zeros(n)
    e[i] = 1
    return e

def resistance_matrix(Q):
    """
    Q is the Laplacian matrix of a graph, as a list of lists
    """
    n = len(Q)
    Qinv = linalg.pinv(Q)
    W = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            unit = unit_vec(i, n) - unit_vec(j, n)
            unitn = np.transpose(unit)
            W[i][j] = unitn @ Qinv @ unit
    return W

def foster_coefficients(Q):
    n = len(Q)
    coeffs = [[0 for _ in range(n)] for _ in range(n)]
    w = resistance_matrix(Q)
    for i in range(n):
        for j in range(n):
            if Q[i][j] < 0:
                coeffs[i][j] = 1 - w[i][j]
    return coeffs

def spanning_tree_count(L):
    """
    L = Laplacian matrix, as a list of lists
    """
    Lred = np.matrix(L)
    Lred = Lred[:-1, :-1]
    kappa = np.linalg.det(Lred)
    return int(np.round(kappa))

def two_forest_count(L):
    """
    L = Laplacian matrix, as a list of lists
    Warning: assumes graph is simple, no loops or parallel edges
    """
    kappa2 = 0
    Lred = np.matrix(L)
    Lred = Lred[:-1, :-1]
    for i in range(len(Lred)):
        # iterate over vertices
        Li = np.delete(Lred, i, axis=0)
        Li = np.delete(Li, i, axis=1)
        kappa_i = np.linalg.det(Li)
        kappa2 += int(np.round(kappa_i))
    for i in range(len(Lred)):
        for j in range(i):
            if Lred[i,j] < 0:
                # iterate over edges
                Lij = np.delete(Lred, [i, j], axis=0)
                Lij = np.delete(Lij, [i, j], axis=1)
                kappa_ij = np.linalg.det(Lij)
                kappa2 -= int(np.round(kappa_ij))
    return kappa2

def tau_constant(L):
    # number of vertices
    n = len(L)
    # count edges
    m = 0
    for i in range(n):
        for j in range(i):
            if L[i][j] < 0:
                m += 1
    # genus
    g = m - n + 1
    kappa = spanning_tree_count(L)
    kappa2 = two_forest_count(L)
    tau = 1.0 / 3 * kappa2 / kappa + 1.0 / 6 * g - 1.0 / 12 * m
    return tau

