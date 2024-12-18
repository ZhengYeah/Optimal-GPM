import numpy as np
import csv
from SW import SW_on_D
from PM import PM_on_D
from src.min_error_mechanism import MinL2Mechanism
from src.distance_metric import l2_distance


endpoint_a, endpoint_b = 0, 6.28
total_piece = 3
epsilon = np.linspace(1, 8, 29, endpoint=True)

distance_SW = np.zeros(len(epsilon))
distance_PM = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW
    p, l = SW_on_D(endpoint_a, endpoint_b, epsilon[i], 0)
    distance_SW[i] = l2_distance(0, endpoint_b, total_piece, p, l, 0)
    # PM
    p, l = PM_on_D(endpoint_a, endpoint_b, epsilon[i], 0)
    distance_PM[i] = l2_distance(endpoint_a, endpoint_b, total_piece, p, l, 0)
    # optimal
    opt_PM = MinL2Mechanism(endpoint_a, endpoint_b, epsilon[i], total_piece)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x=3.14)[1]

fields = ["Epsilon", "SW", "PM", "Optimal"]
filename = "worst-case_circular_L2.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_PM[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
