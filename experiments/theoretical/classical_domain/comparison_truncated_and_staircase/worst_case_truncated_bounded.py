from src.closed_form_mechanism import classical_mechanism_01
from scipy.stats import laplace
from src.distance_metric import l1_distance
import numpy as np

exp = np.e

def error_gpm(epsilon, x):
    p, endpoints = classical_mechanism_01(epsilon, x)
    l_1_error = l1_distance(0, 1, 3, p, endpoints, x)
    return l_1_error

def error_staircase(epsilon, x):
    return exp ** (epsilon / 2) / (exp ** epsilon - 1)

def error_truncated_laplace(epsilon, x):
    lap = laplace(loc=x, scale=1/epsilon)
    expected_error = lap.expect(lambda y: abs(y - x), lb=0, ub=1)
    cdf_0 = lap.cdf(0)
    cdf_1 = 1 - lap.cdf(1)
    return expected_error + cdf_0 * x + cdf_1 * (1 - x)

def error_bounded_laplace(epsilon, x):
    C_q = (1 - np.exp(-epsilon)) / epsilon
    first_item = 2 - (1 + epsilon * x) * np.exp(-epsilon * x)
    second_item = (1 + epsilon * (1 - x)) * np.exp(-epsilon * (1 - x))
    return 1 / C_q * (1 / epsilon ** 2) * (first_item - second_item)

if __name__ == '__main__':
    epsilon = np.linspace(1, 8, 29, endpoint=True)
    # save to csv
    import csv
    filename = f"worst_case_L1.csv"
    with open(filename, "w", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Epsilon", "GPM", "Staircase", "Truncated Laplace", "Bounded Laplace"])
        for i in range(len(epsilon)):
            one_row = [epsilon[i], error_gpm(epsilon[i], 0), error_staircase(epsilon[i], 0), error_truncated_laplace(epsilon[i], 0.5), max(error_bounded_laplace(epsilon[i], 0.), error_bounded_laplace(epsilon[i], 0))]
            csvwriter.writerow(one_row)
