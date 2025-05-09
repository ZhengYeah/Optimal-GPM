from logging import raiseExceptions

import numpy as np
import csv
from PM import PM_on_C
from src.distance_metric import l2_distance
from src.min_error_mechanism import MinL2Mechanism
import math
from scipy.integrate import quad

def error_PM_truncation(epsilon, input_x):
    """
    [-1, 1) -> [-1, 1)
    """
    assert (-1 <= input_x <= 1)
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1
    def integrand(y):
        if -C <= y < left_t:
            return left_right_probability
        elif left_t <= y <= right_t:
            return center_probability
        elif right_t < y <= C:
            return left_right_probability
        else:
            raise ValueError("y is out of bounds")
    def integrand_l2_loss(y):
        if -C <= y < left_t:
            return (y - input_x) ** 2 * left_right_probability
        elif left_t <= y <= right_t:
            return (y - input_x) ** 2 * center_probability
        else:
            return (y - input_x) ** 2 * left_right_probability
    return quad(integrand, -C, -1)[0] * (input_x + 1) ** 2 + quad(integrand, 1, C)[0] * (1 - input_x) ** 2 + quad(integrand_l2_loss, -1, 1)[0]


epsilon = 4
in_endpoint_a, in_endpoint_b = -1, 1
l = PM_on_C(epsilon, in_endpoint_a)[1]
out_endpoint_a, out_endpoint_b = l[0], l[-1]
total_piece = 3
x = np.linspace(-1, 1, 29, endpoint=False)

distance_PM = np.zeros(len(x))
distance_t_PM = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    p, l = PM_on_C(epsilon, x[i])
    distance_PM[i] = l2_distance(out_endpoint_a, out_endpoint_b, total_piece, p, l, x[i])
    distance_t_PM[i] = error_PM_truncation(epsilon, x[i])
    # optimal
    opt_PM = MinL2Mechanism(in_endpoint_a, in_endpoint_b, epsilon, 3)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]


fields = ["x", "PM", "Optimal", "PM_truncation"]
filename = "ablation_whole-domain_L2_PM.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(x)):
        one_row = [x[i], distance_PM[i], distance_optimal[i], distance_t_PM[i]]
        csvwriter.writerow(one_row)
csvfile.close()
