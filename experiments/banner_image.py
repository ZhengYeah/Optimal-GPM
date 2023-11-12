import math
import numpy as np
import csv
from SW import SW_on_01
from L1_distance import L1_distance
from optimal_for_L_1.m_optimal_L1_delta import m_optimal_piecewise

epsilon = np.linspace(1, 8, 29, endpoint=True)
# worst-case error locates at x = 0
distance_SW = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))
distance_delta_DP_optimal = np.zeros((len(epsilon)))
distance_PDP_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW
    p, l = SW_on_01(epsilon[i], 0)
    distance_SW[i] = L1_distance(p, l, 0, 3)
    # optimal piecewise
    distance_optimal[i] = m_optimal_piecewise(epsilon[i], 3, 0)[2]
    # (epsilon, 0.05)-DP
    distance_delta_DP_optimal[i] = m_optimal_piecewise(epsilon[i], 3, 0.05)[2]
    # (epsilon, 0.05)-DP
    distance_PDP_optimal[i] = m_optimal_piecewise(epsilon[i], 3, 0, x=0.05)[2]

fields = ["Epsilon", "SW", "Optimal", "Delta-DP-optimal", "PDP-optimal"]
filename = "banner_image.csv"
with open(filename, "w") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_optimal[i], distance_delta_DP_optimal[i], distance_PDP_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()
