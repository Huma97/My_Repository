import numpy as np
from scipy.special import logsumexp

def get_dists(X):
    """
    X - [N, M] - matrix
    compute pairwise distance matrix for a set of vectors
    """
    x_rows_sum_squared = np.expand_dims(np.sum(np.square(X), axis=1), axis=1)
    # [N, 1]
    # [N, 1] + [1, N] - 2 * [N, N] 
    distances = x_rows_sum_squared + x_rows_sum_squared.T - 2 * np.dot(X, X.T) 
    return distances   

def get_shape(x):
    """
    x - [N, M] matrix, np.array
    """
    dims = float(x.shape[1])
    N = float(x.shape[0])
    return dims, N

def entropy_estimator_kl(x, var):
    # KL-based upper bound on entropy of mixture of Gaussians with covariance matrix var * I 
    #  see Kolchinsky and Tracey, Estimating Mixture Entropy with Pairwise Distances, Entropy, 2017. Section 4.
    #  and Kolchinsky and Tracey, Nonlinear Information Bottleneck, 2017. Eq. 10
    dims, N = get_shape(x)
    dists = get_dists(x)
    dists2 = dists / (2*var)
    normconst = (dims/2.0)*np.log(2*np.pi*var)
    lprobs = logsumexp(-dists2, axis=1) - np.log(N) - normconst
    h = -np.mean(lprobs)
    return dims/2 + h

def entropy_estimator_bd(x, var):
    # Bhattacharyya-based lower bound on entropy of mixture of Gaussians with covariance matrix var * I 
    #  see Kolchinsky and Tracey, Estimating Mixture Entropy with Pairwise Distances, Entropy, 2017. Section 4.
    dims, N = get_shape(x)
    val = entropy_estimator_kl(x,4*var)
    return val + np.log(0.25)*dims/2

def kde_condentropy(output, var):
    # Return entropy of a multivariate Gaussian, in nats
    dims = output.shape[1]
    return (dims/2.0)*(np.log(2*np.pi*var) + 1)