import numpy as np
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1])) # Adjust the path to include the src directory
from src.closed_form_mechanism import classical_mechanism_01
from src.distance_metric import l1_distance
from scipy.stats import laplace
# Set up the plotting environment
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

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

x = np.linspace(0, 1, 50, endpoint=False)
epsilon = 2
error_gpm_values = np.zeros(len(x))
error_staircase_values = np.zeros(len(x))
error_truncated_laplace_values = np.zeros(len(x))
error_bounded_laplace_values = np.zeros(len(x))
for i in range(len(x)):
    error_gpm_values[i] = error_gpm(epsilon, x[i])
    error_staircase_values[i] = error_staircase(epsilon, x[i])
    error_truncated_laplace_values[i] = error_truncated_laplace(epsilon, x[i])
    error_bounded_laplace_values[i] = error_bounded_laplace(epsilon, x[i])
plt.figure(figsize=(5, 4))
plt.plot(x, error_staircase_values, label='Staircase', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(x, error_truncated_laplace_values, label='T-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8, markevery=2)
plt.plot(x, error_bounded_laplace_values, label='B-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='x', markersize=8, markevery=2)
plt.plot(x, error_gpm_values, label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Input $x$')
plt.ylabel(r'Absolute error')
plt.xticks(np.arange(0, 1.1, 0.2))
plt.yticks(np.arange(0, 0.45, 0.1))
plt.ylim(0, 0.45)
plt.legend(loc='lower right')
plt.title('Figure 13a')

######## End of Figure 13a ########

epsilon = np.linspace(1, 8, 29, endpoint=True)
error_gpm_values = np.zeros(len(epsilon))
error_staircase_values = np.zeros(len(epsilon))
error_truncated_laplace_values = np.zeros(len(epsilon))
error_bounded_laplace_values = np.zeros(len(epsilon))
for i in range(len(epsilon)):
    error_gpm_values[i] = error_gpm(epsilon[i], 0)
    error_staircase_values[i] = error_staircase(epsilon[i], 0)
    error_truncated_laplace_values[i] = error_truncated_laplace(epsilon[i], 0.5)
    error_bounded_laplace_values[i] = max(error_bounded_laplace(epsilon[i], 0.), error_bounded_laplace(epsilon[i], 0))
plt.figure(figsize=(5, 4))
plt.plot(epsilon, error_staircase_values, label='Staircase', linewidth=2, linestyle='--', color=[0, 0, 0])
plt.plot(epsilon, error_truncated_laplace_values, label='T-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(epsilon, error_bounded_laplace_values, label='B-Laplace', linewidth=2, linestyle='-', color=[0, 0, 1], marker='x', markersize=8)
plt.plot(epsilon, error_gpm_values, label='GPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.ylabel(r'Worst-case error')
plt.xticks(np.arange(1, 9, 1))
plt.yticks(np.arange(0, 1, 0.2))
plt.ylim(0, 1)
plt.legend(loc='upper right')
plt.title('Figure 14')

######## End of Figure 14 ########

from src.min_error_mechanism import MinL1Mechanism
pi = np.pi

def purkayastha_error(epsilon):
    """
    Calculate the Purkayastha error for a given epsilon.
    The formula is derived from the paper "Differential Privacy for Directional Data" (CCS'21).
    """
    # Purkayastha error is defined as:
    # pur_error = 2 * k * A_l + reminder
    # where k = epsilon / pi, A_l = 1 / (k ** 2), and reminder = pi / (1 - exp ** (k * pi)) - 1 / k
    # m = 1, so l has only one value 1
    k = epsilon / pi
    reminder = pi / (1 - exp ** (k * pi)) - 1 / k
    A_l = 1 / (k ** 2)
    pur_error = 2 * k * A_l + reminder
    return pur_error

def ogpm_circular_error(epsilon):
    ogpm = MinL1Mechanism(0, 2 * pi, epsilon, 3)
    ogpm.solve_probabilities()
    return ogpm.solve_lr(x=pi)[1]

epsilon = np.linspace(1, 8, 29, endpoint=True)
purkayastha_distance = np.zeros(len(epsilon))
ogpm_distance = np.zeros(len(epsilon))
for i, _ in enumerate(epsilon):
    purkayastha_distance[i] = purkayastha_error(epsilon[i])
    ogpm_distance[i] = ogpm_circular_error(epsilon[i])
plt.figure(figsize=(5, 4))
plt.plot(epsilon, purkayastha_distance, label=r'Pur$(n=2,\kappa)$',linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
plt.plot(epsilon, ogpm_distance, label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
plt.xlabel(r'Privacy parameter $\varepsilon$')
plt.xticks(np.arange(1, 9, 1))
plt.yticks(np.arange(0, 1.6, 0.5))
plt.legend(loc='upper right')
plt.title('Figure 15')
plt.show()

######## End of Figure 15 ########
