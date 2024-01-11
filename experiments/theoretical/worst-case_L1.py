import numpy as np
import csv
from SW import SW_on_01
from PM import PM_on_01
from src.min_error_mechanism import MinL1Mechanism
from src.distance_metric import l1_distance

epsilon = np.linspace(1, 8, 29, endpoint=True)

distance_SW = np.zeros(len(epsilon))
distance_PM = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW
    p, l = SW_on_01(epsilon[i], 0)
    distance_SW[i] = l1_distance(0, 1, 3, p, l, 0)
    # PM
    p, l = PM_on_01(epsilon[i], 0)
    distance_PM[i] = l1_distance(0, 1, 3, p, l, 0)
    # optimal
    opt_PM = MinL1Mechanism(endpoint_a=0, endpoint_b=1, epsilon=epsilon[i], total_piece=3)
    distance_optimal[i] = opt_PM.solve_probabilities()[2]

fields = ["Epsilon", "SW", "PM", "Optimal"]
filename = "worst-case_L1.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_PM[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
