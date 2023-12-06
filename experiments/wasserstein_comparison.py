import numpy as np
import csv
from SW import SW_on_01
from PM import PM_on_01
from wasserstein_distance import wasserstein_distance
from m_optimal_Wasserstein import min_wasserstein_mechanism


def endpoints_to_lengths(endpoints):
    res = np.zeros(len(endpoints) - 1)
    for i in range(len(endpoints) - 1):
        res[i] = endpoints[i + 1] - endpoints[i]
    return res

epsilon = np.linspace(1, 8, 29, endpoint=True)
# worst-case error locates at x = 0
distance_SW = np.zeros(len(epsilon))
distance_PM = np.zeros(len(epsilon))
distance_optimal = np.zeros((len(epsilon)))
distance_delta_DP_optimal = np.zeros((len(epsilon)))
distance_PDP_optimal = np.zeros((len(epsilon)))

for i, _ in enumerate(epsilon):
    # SW
    p, l = SW_on_01(epsilon[i], 0)
    l = endpoints_to_lengths(l)
    distance_SW[i] = wasserstein_distance(p, l, 0, 3)
    # PM
    p, l = PM_on_01(epsilon[i], 0)
    l = endpoints_to_lengths(l)
    distance_PM[i] = wasserstein_distance(p, l, 0, 3)
    # optimal piecewise
    distance_optimal[i] = min_wasserstein_mechanism(epsilon[i], 3, 0)[2]
    # (epsilon, 0.05)-DP
    distance_delta_DP_optimal[i] = min_wasserstein_mechanism(epsilon[i], 3, 0.05)[2]
    # (epsilon, 0.05)-PDP
    distance_PDP_optimal[i] = 0.95 * min_wasserstein_mechanism(epsilon[i], 3, 0)[2]

fields = ["Epsilon", "SW", "PM", "Optimal", "Delta-DP-optimal", "PDP-optimal"]
filename = "wasserstein_comparison.csv"
with open(filename, "w", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    for i in range(len(epsilon)):
        one_row = [epsilon[i], distance_SW[i], distance_PM[i], distance_optimal[i], distance_delta_DP_optimal[i], distance_PDP_optimal[i]]
        csvwriter.writerow(one_row)
csvfile.close()



