import math
import numpy as np
from recycle_bin.L1_distance import l1_distance

def SW_on_01(epsilon, input_x):
    assert (0 <= input_x <= 1)
    b = (epsilon * math.exp(epsilon) - math.exp(epsilon) + 1) / (2 * math.exp(epsilon) * (math.exp(epsilon) - 1 - epsilon))
    central_probability = math.exp(epsilon) / (2 * b * math.exp(epsilon) + 1)
    left_right_probability = 1 / (2 * b * math.exp(epsilon) + 1)

    central_probability = central_probability * (1 + 2 * b)
    left_right_probability = left_right_probability * (1 + 2 * b)
    left_t = input_x / (1 + 2 * b)
    right_t = (input_x + 2 * b) / (1 + 2 * b)
    interval_endpoint = [0, left_t, right_t, 1]
    interval_probability = [left_right_probability, central_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint


def SW(epsilon, input_x):
    assert (0 <= input_x <= 1)
    b = (epsilon * math.exp(epsilon) - math.exp(epsilon) + 1) / (2 * math.exp(epsilon) * (math.exp(epsilon) - 1 - epsilon))
    central_probability = math.exp(epsilon) / (2 * b * math.exp(epsilon) + 1)
    left_right_probability = 1 / (2 * b * math.exp(epsilon) + 1)
    interval_endpoint = [-b, input_x - b, input_x + b, 1 + b]
    interval_probability = [left_right_probability, central_probability, left_right_probability]
    return interval_probability, interval_endpoint


if __name__ == "__main__":
    x = np.linspace(0, 1, 10, endpoint=False)
    # x = [0]
    for i, _ in enumerate(x):
        interval_probability, interval_endpoint = SW(1, x[i])
        distance = l1_distance(interval_probability, interval_endpoint, x[i], 3)
        print(f"L_1 distance: {distance}")
