import numpy as np
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1])) # Adjust the path to include the src directory
from src.PM import PM_on_C
from src.SW import SW
from src.distance_metric import l2_distance
from src.min_error_mechanism import MinL2Mechanism
import math
from scipy.integrate import quad
# Set up the plotting environment
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'


def error_PM_truncation(epsilon, input_x):
    r"""
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

epsilon = 2
in_endpoint_a, in_endpoint_b = -1, 1
l = PM_on_C(epsilon, in_endpoint_a)[1]
out_endpoint_a, out_endpoint_b = l[0], l[-1]
total_piece = 3
x = np.linspace(-1, 1, 29, endpoint=False)

distance_PM = np.zeros(len(x))
distance_t_PM = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))
for i, _ in enumerate(x):
    # PM
    p, l = PM_on_C(epsilon, x[i])
    distance_PM[i] = l2_distance(out_endpoint_a, out_endpoint_b, total_piece, p, l, x[i])
    distance_t_PM[i] = error_PM_truncation(epsilon, x[i])
    # optimal
    opt_PM = MinL2Mechanism(in_endpoint_a, in_endpoint_b, epsilon, 3)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]
plt.figure(figsize=(5, 4))
plt.plot(x, distance_PM, label='PM', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(x, distance_t_PM, label='PM-truncation', linewidth=2, linestyle='--', color=[0, 0, 1], marker='.', markersize=8, markevery=2)
plt.plot(x, distance_optimal, label='OGPM on [-1, 1]', linestyle='-', color=[1, 0, 0])
plt.xticks(np.arange(-1, 1.1, 0.5))
plt.yticks(np.arange(0, 1.2, 0.2))
plt.ylim(0, 1.2)
plt.legend(loc='upper right')
plt.title('Figure 12a')

######## End of Figure 12a ########

def error_SW_truncation(epsilon, input_x):
    r"""
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

epsilon = 2
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
    # optimal
    opt_PM = MinL2Mechanism(in_endpoint_a, in_endpoint_b, epsilon, 3)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]
plt.figure(figsize=(5, 4))
plt.plot(x, distance_SW, label='SW', linewidth=2, linestyle='--', color=[0, 0, 0], marker='+', markersize=8, markevery=3)
plt.plot(x, distance_t_SW, label='SW-truncation', linewidth=2, linestyle='--', color=[0, 0, 0], marker='.', markersize=8, markevery=2)
plt.plot(x, distance_optimal, label='OGPM', linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Squared error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.18, 0.1))
plt.ylim(0, 0.18)
plt.legend(loc='upper right')
plt.title('Figure 12b')
plt.show()

######## End of Figure 12b ########
