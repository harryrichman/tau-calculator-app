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
