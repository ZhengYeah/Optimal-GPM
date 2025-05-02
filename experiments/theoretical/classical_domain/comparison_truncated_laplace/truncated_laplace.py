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
    lap = laplace(loc=x, scale=1/epsilon)
    expected_error = lap.expect(lambda y: abs(y - x), lb=0, ub=1)
    cdf_0 = lap.cdf(0)
    cdf_1 = 1 - lap.cdf(1)
    return expected_error + cdf_0 * x + cdf_1 * (1 - x)

if __name__ == '__main__':
    x = np.linspace(0, 1, 20, endpoint=False)
    epsilon = 2
    # save to csv
    import csv
    filename = "truncated_laplace.csv"
    with open(filename, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["x", "GPM", "Laplace", "Truncated Laplace"])
        for i in range(len(x)):
            one_row = [x[i], error_gpm(epsilon, x[i]), error_laplace(epsilon, x[i]), error_truncated_laplace(epsilon, x[i])]
            csvwriter.writerow(one_row)
    csvfile.close()

