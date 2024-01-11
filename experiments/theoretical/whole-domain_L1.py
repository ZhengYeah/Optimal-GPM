import numpy as np
import csv
from SW import SW_on_01
from PM import PM_on_01
from recycle_bin.L1_distance import l1_distance
from src.min_error_mechanism import MinL1Mechanism

x = np.linspace(0, 1, 29, endpoint=False)

distance_SW = np.zeros(len(x))
distance_PM = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    # SW
    p, l = SW_on_01(x[i], 0)
    distance_SW[i] = l1_distance(p, l, 0, 3)
    # PM
    p, l = PM_on_01(x[i], 0)
    distance_PM[i] = l1_distance(p, l, 0, 3)
    # optimal
    opt_PM = MinL1Mechanism(endpoint_a=0, endpoint_b=1, epsilon=1, total_piece=3)
    opt_PM.solve_probabilities()
    opt_distance = opt_PM.solve_lr(x[i])


fields = ["Epsilon", "SW", "PM", "Optimal"]
filename = "worst-case_L1.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_PM[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
