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

def error_truncated_laplace_05(epsilon, input_x=0.5):
    # error_0_1 = (1 - exp ** (-epsilon) * (1 + epsilon)) / epsilon
    error_0_1 = laplace.expect(lambda x: abs(x), scale=1/epsilon, lb=-0.5, ub=0.5)
    cdf_1_infty = laplace.cdf(-0.5, scale=1/epsilon) * 0.5
    return error_0_1 + cdf_1_infty * 2


if __name__ == '__main__':
    x = 0.5
    epsilon = range(1, 10)
    error_gpm_list = [error_gpm(e, x) for e in epsilon]
    error_laplace_list = [error_laplace(e, x) for e in epsilon]
    error_truncated_laplace_list = [error_truncated_laplace_05(e, x) for e in epsilon]
    # write to csv
    import csv
    with open('comparison_laplace.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['epsilon', 'error_gpm', 'error_laplace', 'error_truncated_laplace'])
        for i in range(len(epsilon)):
            writer.writerow([epsilon[i], error_gpm_list[i], error_laplace_list[i], error_truncated_laplace_list[i]])
