import numpy as np
import csv
from SW import SW
from PM import PM_on_C
from src.distance_metric import l2_distance
from src.min_error_mechanism import MinL2MechanismAblation


epsilon = 4
in_endpoint_a, in_endpoint_b = -1, 1
l = PM_on_C(epsilon, in_endpoint_a)[1]
out_endpoint_a, out_endpoint_b = l[0], l[-1]
total_piece = 3
x = np.linspace(0, 1, 29, endpoint=False)

distance_SW = np.zeros(len(x))
distance_PM = np.zeros(len(x))
distance_optimal = np.zeros((len(x)))

for i, _ in enumerate(x):
    # # SW
    # p, l = SW(epsilon, x[i])
    # distance_SW[i] = l2_distance(out_endpoint_a, out_endpoint_b, total_piece, p, l, x[i])
    # PM
    p, l = PM_on_C(epsilon, x[i])
    distance_PM[i] = l2_distance(out_endpoint_a, out_endpoint_b, total_piece, p, l, x[i])
    # optimal
    opt_PM = MinL2MechanismAblation(in_endpoint_a, in_endpoint_b, out_endpoint_a, out_endpoint_b, epsilon, total_piece)
    opt_PM.solve_probabilities()
    distance_optimal[i] = opt_PM.solve_lr(x[i])[1]


fields = ["x", "PM", "Optimal"]
filename = "ablation_whole-domain_l2_PM.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(x)):
        one_row = [x[i], distance_PM[i], distance_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
