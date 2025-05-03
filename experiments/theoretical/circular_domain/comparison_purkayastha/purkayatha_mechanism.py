import numpy as np
import csv
from src.min_error_mechanism import MinL1Mechanism


pi = np.pi
exp = np.e

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
fields = ["Epsilon", "PurKayastha", "OGPM"]
filename = "comparison_purkayastha_mechanism.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], purkayastha_distance[i], ogpm_distance[i]]
        csvwriter.writerow(one_row)
