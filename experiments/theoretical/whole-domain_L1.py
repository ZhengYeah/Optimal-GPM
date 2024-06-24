import numpy as np
import csv
from SW import SW_on_01
from PM import PM_on_01
from src.distance_metric import l1_distance
from src.min_error_mechanism import MinL1Mechanism


epsilon = 3
endpoint_a, endpoint_b = 0, 1
total_piece = 3
x = np.linspace(0, 1, 49, endpoint=False)

distance_SW = np.zeros(len(x))
distance_PM = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    # SW
    p, l = SW_on_01(epsilon, x[i])
    distance_SW[i] = l1_distance(endpoint_a, endpoint_b, total_piece, p, l, x[i])
    # PM
    p, l = PM_on_01(epsilon, x[i])
    distance_PM[i] = l1_distance(endpoint_a, endpoint_b, total_piece, p, l, x[i])
    # optimal
    opt_PM = MinL1Mechanism(endpoint_a, endpoint_b, epsilon, total_piece)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]


fields = ["x", "SW", "PM", "Optimal"]
filename = "whole-domain_L1.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(x)):
        one_row = [x[i], distance_SW[i], distance_PM[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
