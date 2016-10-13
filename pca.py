__author__ = 'minh'

from pylab import *
from sklearn.decomposition import PCA as sklearnPCA

"""
Perform PCA given data points (each point corresponds to one row) and corresponding labels
"""
def do_pca(data, dim=2):
    sklearn_pca = sklearnPCA(n_components=dim)
    data = np.matrix(data)

    # normalize data
    (n, d) = data.shape;
    data = data - np.tile(np.mean(data, 0), (n, 1));

    Y = sklearn_pca.fit_transform(data)
    return Y