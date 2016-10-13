__author__ = 'minh'

"""
This function runs tsne
input P: pairwise similarity / distance matrix
input d: latent space dimensionality number (2-D, 3-D)
output: coordinates of data points on latent space

Citation:
Maaten, Laurens van der, and Geoffrey Hinton. "Visualizing data using t-SNE." Journal of Machine Learning Research 9.Nov (2008): 2579-2605.
"""

import numpy as Math
from pylab import *
from sklearn.manifold import TSNE

"""
MTSNE_SIMILARITY = 0: run tsne using distance matrix
MTSNE_SIMILARITY = 1: run tsne using similarity matrix
Default is 1
"""
MTSNE_SIMILARITY = 0



"""
Run tsne using similarity matrix (eg. EROS)
Output coordinates of data points on latent space
"""
def similarity_tsne(P, no_dims=2):
    """Runs t-SNE on the dataset in the NxD array X to reduce its dimensionality to no_dims dimensions.
    The syntaxis of the function is Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array."""

    # Check inputs
    if isinstance(no_dims, float):
        print "Error: array X should have type float.";
        return -1;
    if round(no_dims) != no_dims:
        print "Error: number of dimensions should be an integer.";
        return -1;

    max_iter = 1000;
    initial_momentum = 0.5;
    final_momentum = 0.8;
    eta = 500;
    min_gain = 0.01;

    (n, d) = P.shape;
    Math.random.seed(seed=500)
    Y = Math.random.randn(n, no_dims);
    dY = Math.zeros((n, no_dims));
    iY = Math.zeros((n, no_dims));
    gains = Math.ones((n, no_dims));

    # set digonal to zero
    for i in range(n):
        P[i, i] = 0

    P = (P + Math.transpose(P)) / 2;
    P = P / Math.sum(P);
    P = P * 4;
    P = Math.maximum(P, 1e-12);

    # Run iterations
    for iter in range(max_iter):

        # Compute pairwise affinities
        sum_Y = Math.sum(Math.square(Y), 1);
        num = 1 / (1 + Math.add(Math.add(-2 * Math.dot(Y, Y.T), sum_Y).T, sum_Y));
        num[range(n), range(n)] = 0;
        Q = num / Math.sum(num);
        Q = Math.maximum(Q, 1e-12);

        # Compute gradient
        PQ = P - Q;
        for i in range(n):
            dY[i, :] = Math.sum(Math.tile(PQ[:, i] * num[:, i], (no_dims, 1)).T * (Y[i, :] - Y), 0);

        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((dY > 0) != (iY > 0)) + (gains * 0.8) * ((dY > 0) == (iY > 0));
        gains[gains < min_gain] = min_gain;
        iY = momentum * iY - eta * (gains * dY);
        Y = Y + iY;
        Y = Y - Math.tile(Math.mean(Y, 0), (n, 1));

        # Compute current value of cost function
        if (iter + 1) % 10 == 0:
            C = Math.sum(P * Math.log(P / Q));
            print "Iteration ", (iter + 1), ": error is ", C

        # Stop lying about P-values
        if iter == 100:
            P = P / 4;

    # Return solution
    return Y;



"""
Run tsne using distance matrix (eg. EROS)
Output coordinates of data points on latent space
"""
def distance_tsne(distance_matrix, d=2, perplexity=10):
    # If the metric is 'precomputed' X must be a square distance matrix. Otherwise it contains a sample per row.
    model = TSNE(metric='precomputed', n_components=d, random_state=10, n_iter=1000, perplexity=perplexity)
    Y = model.fit_transform(distance_matrix)
    return Y



"""
main function
"""
def mtsne(P, d=2):
    if MTSNE_SIMILARITY==0:
        Y = distance_tsne(P, d, perplexity=20)
    else:
        Y = similarity_tsne(P, d)
    return Y


