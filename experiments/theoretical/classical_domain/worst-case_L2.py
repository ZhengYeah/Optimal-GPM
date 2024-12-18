import numpy as np
import csv
from SW import SW_on_01, SW
from PM import PM_on_01, PM_trans_01
from src.closed_form_mechanism import unbias_gpm
from src.min_error_mechanism import MinL2Mechanism
from src.distance_metric import l2_distance


endpoint_a, endpoint_b = 0, 1
total_piece = 3
epsilon = np.linspace(1, 8, 29, endpoint=True)

distance_SW = np.zeros(len(epsilon))
distance_SW_C = np.zeros(len(epsilon))
distance_PM = np.zeros(len(epsilon))
distance_PM_C = np.zeros(len(epsilon))
distance_unbias_gpm = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW
    p, l = SW(epsilon[i], 0)
    distance_SW[i] = l2_distance(l[0], l[-1], total_piece, p, l, 0)
    # SW-C
    p, l = SW_on_01(epsilon[i], 0)
    distance_SW_C[i] = l2_distance(endpoint_a, endpoint_b, total_piece, p, l, 0)
    # PM
    p, l = PM_trans_01(epsilon[i], 0)
    distance_PM[i] = l2_distance(l[0], l[-1], total_piece, p, l, 0)
    # PM-C
    p, l = PM_on_01(epsilon[i], 0)
    distance_PM_C[i] = l2_distance(endpoint_a, endpoint_b, total_piece, p, l, 0)
    # unbias_gpm
    p, l = unbias_gpm(epsilon[i], 0)
    distance_unbias_gpm[i] = l2_distance(l[0], l[-1], total_piece, p, l, 0)
    # optimal
    opt_PM = MinL2Mechanism(endpoint_a, endpoint_b, epsilon[i], total_piece)
    distance_optimal[i] = opt_PM.solve_probabilities()[2]

fields = ["Epsilon", "SW", "SW-C", "PM", "PM-C", "Unbias-GPM", "Optimal"]
filename = "worst-case_L2.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_SW_C[i], distance_PM[i], distance_PM_C[i], distance_unbias_gpm[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
