from src.closed_form_mechanism import classical_mechanism_01
from scipy.stats import laplace
from src.distance_metric import l1_distance
import numpy as np

exp = np.e

def error_gpm(epsilon, x):
    p, endpoints = classical_mechanism_01(epsilon, x)
    l_1_error = l1_distance(0, 1, 3, p, endpoints, x)
    return l_1_error

def error_laplace(epsilon, x):
    return 1 / epsilon

def error_truncated_laplace(epsilon, x):
    error_0_1 = (1 - exp ** (-epsilon) * (1 + epsilon)) / epsilon
    cdf_1_infty = laplace.cdf(-1, scale=1/epsilon) * 1
    return error_0_1 + cdf_1_infty * 2


if __name__ == '__main__':
    x = 0.5
    epsilon = 5
    print(error_gpm(epsilon, x))
    print(error_laplace(epsilon, x))
    print(error_truncated_laplace(epsilon, x))



