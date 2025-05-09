import numpy as np
import csv
from SW import SW
from src.distance_metric import l2_distance
from src.min_error_mechanism import MinL2Mechanism
import math
from scipy.integrate import quad


def error_SW_truncation(epsilon, input_x):
    """
    [0, 1) -> [0, 1)
    """
    assert (0 <= input_x <= 1)
    b = (epsilon * math.exp(epsilon) - math.exp(epsilon) + 1) / (2 * math.exp(epsilon) * (math.exp(epsilon) - 1 - epsilon))
    central_probability = math.exp(epsilon) / (2 * b * math.exp(epsilon) + 1)
    left_right_probability = 1 / (2 * b * math.exp(epsilon) + 1)
    p, l = SW(epsilon, input_x)
    def integrand(y):
        if y < input_x - b:
            return left_right_probability
        elif input_x - b <= y <= input_x + b:
            return central_probability
        else:
            return left_right_probability
    def integrand_l2_loss(y):
        if y < input_x - b:
            return (y - input_x) ** 2 * left_right_probability
        elif input_x - b <= y <= input_x + b:
            return (y - input_x) ** 2 * central_probability
        else:
            return (y - input_x) ** 2 * left_right_probability
    return quad(integrand, -b, 0)[0] * (input_x - 0) ** 2 + quad(integrand, 1, 1 + b)[0] * (1 - input_x) ** 2 + quad(integrand_l2_loss, 0, 1)[0]

epsilon = 4
in_endpoint_a, in_endpoint_b = 0, 1
l = SW(epsilon, in_endpoint_a)[1]
out_endpoint_a, out_endpoint_b = l[0], l[-1]
total_piece = 3
x = np.linspace(0, 1, 29, endpoint=False)

distance_SW = np.zeros(len(x))
distance_t_SW = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    # SW
    p, l = SW(epsilon, x[i])
    distance_SW[i] = l2_distance(out_endpoint_a, out_endpoint_b, total_piece, p, l, x[i])
    distance_t_SW[i] = error_SW_truncation(epsilon, x[i])
    opt_PM = MinL2Mechanism(in_endpoint_a, in_endpoint_b, epsilon, 3)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]


fields = ["x", "SW", "Optimal", "SW_truncation"]
filename = "ablation_whole-domain_l2_SW.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(x)):
        one_row = [x[i], distance_SW[i], distance_optimal[i], distance_t_SW[i]]
        csvwriter.writerow(one_row)
csvfile.close()
