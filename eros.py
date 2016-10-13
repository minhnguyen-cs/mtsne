__author__ = 'minh'

"""
This function computes the EROS pairwise PCA-based similarity matrix
input myData: Array of matrices (array of multivariate timeseries)
output dist: Pairwise similarity matrix
        [
        [1       x01     x02]
        [x01     1       x12]
        [x02     x12     1  ]
        ]

Citation:
Kiyoung Yang and Cyrus Shahabi, A PCA-based Similarity Measure for Multivariate Time Series, The Second ACM International Workshop on Multimedia Databases (ACM-MMDB 2004), pp 65 - 74 , ISBN:1-58113-975-6, Washington D.C., U.S.A., November 2004
"""

import numpy as np

"""
Compute eigen values and eigen vectors of a matrix
"""
def pca(data):
    # data-centering
    data -= data.mean(axis=0)

    # covariance matrix
    R = np.cov(data, rowvar=False)

    # get eigen vectors and eigen values from the covariance matrix R
    evals, evecs = np.linalg.eigh(R)
    return evals, evecs

"""
Normalizaing eigen values in the eigen value matrix
"""
def normalizeEvals(evals):
    for i in range(0, len(evals)):
        for j in range(0, len(evals[i])):
            evals[i][j] = evals[i][j] / sum(evals[i])
    return evals


"""
compute weight vector from eigen values
"""
def weight_vector(evals):
    weight = []

    # compute mean of each column/variable
    for j in range(0, len(evals[0])):
        mean_val = np.mean(map(float, [evals[i][j] for i in range(0, len(evals))]))
        weight.append(mean_val)

    # normalize weight vector
    total_weight = sum(weight)
    normed_weight_vector = [float(i) / total_weight for i in weight]
    return normed_weight_vector


"""
compute the eros pairwise similarity of an array of matrices
"""
def eros(data):
    # compute eigen values and vectors for each matrix
    evals, evecs = [], []
    for i in range(0, len(data)):
        _vals, _vecs = pca(data[i])
        evals.append(_vals)
        evecs.append(np.matrix(_vecs))

    # normalize eigen value to compute weight vector (optional)
    # normEvals = evals
    # normalize eigen value
    # normEvals = normalizeEvals(evals)

    # compute weight vector (defined in the paper)
    w = weight_vector(evals)

    """
    compute pairwise SIMILARITY matrix
    """
    # init similarity matrix
    sim_matrix = np.matrix(np.zeros(shape=(len(evecs), len(evecs), 1)))

    for i in range(0, len(evecs)):
        for j in range(0, len(evecs)):
            if i == j:
                sim_matrix[i, j] = 1
                continue
            if j < i:
                sim_matrix[i, j] = sim_matrix[j, i]
                continue
            # compute pairwise similarity between evecs[i] and evecs[j]
            sim_matrix[i, j] = np.sum([float(
                w[n] * np.abs(np.inner(np.squeeze(np.asarray(evecs[i][:, n])), np.squeeze(np.asarray(evecs[j][:, n])))))
                                       for n in range(0, len(evecs[i]))])
    return (sim_matrix)
