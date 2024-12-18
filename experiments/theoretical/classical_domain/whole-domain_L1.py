import numpy as np
import csv
from SW import SW_on_01, SW
from PM import PM_on_01, PM_trans_01
from src.closed_form_mechanism import unbias_gpm
from src.distance_metric import l1_distance
from src.min_error_mechanism import MinL1Mechanism


epsilon = 4
endpoint_a, endpoint_b = 0, 1
total_piece = 3
x = np.linspace(0, 1, 49, endpoint=False)

distance_SW = np.zeros(len(x))
distance_SW_C = np.zeros(len(x))
distance_PM = np.zeros(len(x))
distance_PM_C = np.zeros(len(x))
distance_unbias_gpm = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    # SW-C
    p, l = SW_on_01(epsilon, x[i])
    distance_SW_C[i] = l1_distance(endpoint_a, endpoint_b, total_piece, p, l, x[i])
    # SW
    p, l = SW(epsilon, x[i])
    distance_SW[i] = l1_distance(l[0], l[-1], total_piece, p, l, x[i])
    # PM-C
    p, l = PM_on_01(epsilon, x[i])
    distance_PM_C[i] = l1_distance(endpoint_a, endpoint_b, total_piece, p, l, x[i])
    # PM
    p, l = PM_trans_01(epsilon, x[i])
    distance_PM[i] = l1_distance(l[0], l[-1], total_piece, p, l, x[i])
    # unbias_gpm
    p, l = unbias_gpm(epsilon, x[i])
    distance_unbias_gpm[i] = l1_distance(l[0], l[-1], total_piece, p, l, x[i])
    # optimal
    opt_PM = MinL1Mechanism(endpoint_a, endpoint_b, epsilon, total_piece)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]


fields = ["x", "SW", "SW-C", "PM", "PM-C", "Unbias-GPM", "Optimal"]
# file for the given epsilon
filename = "whole_domain_L1_" + str(epsilon) + ".csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(x)):
        one_row = [x[i], distance_SW[i], distance_SW_C[i], distance_PM[i], distance_PM_C[i], distance_unbias_gpm[i],distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
