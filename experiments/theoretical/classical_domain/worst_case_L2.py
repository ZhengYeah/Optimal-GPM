import numpy as np
import csv
from src.SW import SW_on_01
from src.PM import PM_on_01
from src.min_error_mechanism import MinL2Mechanism
from src.distance_metric import l2_distance


endpoint_a, endpoint_b = 0, 1
total_piece = 3
epsilon = np.linspace(1, 8, 29, endpoint=True)

distance_SW_C = np.zeros(len(epsilon))
distance_PM_C = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW-C
    p, l = SW_on_01(epsilon[i], 0)
    distance_SW_C[i] = l2_distance(endpoint_a, endpoint_b, total_piece, p, l, 0)
    # PM-C
    p, l = PM_on_01(epsilon[i], 0)
    distance_PM_C[i] = l2_distance(endpoint_a, endpoint_b, total_piece, p, l, 0)
    # optimal
    opt_PM = MinL2Mechanism(endpoint_a, endpoint_b, epsilon[i], total_piece)
    distance_optimal[i] = opt_PM.solve_probabilities()[2]

fields = ["Epsilon", "SW-C", "PM-C", "Optimal"]
filename = "worst_case_L2.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW_C[i], distance_PM_C[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
