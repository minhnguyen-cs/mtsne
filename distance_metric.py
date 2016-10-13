__author__ = 'minh'

import math
import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

"""
Compute distance matrix from (multivariate) time series data using Euclidean distance
"""
def eu_distance_matrix(data, distance_file, squared = True):
    matrix = []
    for i in range(len(data)):
        for j in range(len(data)):
            if i == j:
                matrix.append(0)
                continue

            if j < i:
                matrix.append(matrix[j * len(data) + i])
                continue

            #norm distance between 2 matrices
            if data[i].shape != data[j].shape:
                raise ValueError('Missing value! 2 matrices not the same length: '+ str(i) + ' (length='+ str(len(data[i])) + ') and ' + str(j)
                                 + ' (length='+ str(len(data[j])) + ')')
            else:
                distance = pow(np.linalg.norm(data[i] - data[j]),2)
                matrix.append(distance)

    matrix = np.array(matrix)
    size = int(math.sqrt(len(matrix)))
    matrix = matrix.reshape(size, size)

    #save dtw distance into files for further
    if True:
        np.savetxt(distance_file + "_ed", np.array(matrix), delimiter='\t')

    return matrix



"""
Compute distance matrix from (univariate) time series data using dynamic time warping
"""
def dtw_distance_matrix(data, distance_file, recompute = True):
    if not recompute:
        return np.loadtxt(distance_file, delimiter='\t')

    matrix = []
    print 'Computing distance matrix using fastDTW:'
    for i in range(len(data)):
        print 'step ' + str(i) + '/' + str(len(data))
        for j in range(len(data)):
            if i == j:
                matrix.append(0)
                continue
            if j < i:
                matrix.append(matrix[j * len(data) + i])
                continue

            #modified
            distance, path = fastdtw(np.array(data[i]), data[j], dist=euclidean)
            matrix.append(distance)

    matrix = np.array(matrix)
    size = int(math.sqrt(len(matrix)))
    matrix = matrix.reshape(size, size)

    #save dtw distance into files for further
    if True:
        np.savetxt(distance_file + "_dtw", np.array(matrix), delimiter='\t')

    return matrix
