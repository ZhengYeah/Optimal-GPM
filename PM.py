import math
import numpy as np
from L1_distance import l1_distance


def in_machine_error(result, expectation):
    if abs(result - expectation) <= np.finfo(float).eps:
        return expectation
    else:
        return result

def PM_on_02pi(epsilon, input_x):
    assert (0 <= input_x <= 6.28)
    # input mapping
    x = input_x
    input_x = (input_x - 0.5) * 2

    # PM
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    # [0, 1]-PM
    left_t = left_t / (2 * C) + 0.5
    right_t = right_t / (2 * C) + 0.5
    left_t = in_machine_error(left_t, 0)
    right_t = in_machine_error(right_t, 1)
    left_right_probability = left_right_probability * (2 * C)
    center_probability = center_probability * (2 * C)

    interval_endpoint = [0, left_t, right_t, 1]
    interval_probability = [left_right_probability, center_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint


def PM_on_01(epsilon, input_x):
    assert (0 <= input_x <= 1)
    # input mapping
    x = input_x
    input_x = (input_x - 0.5) * 2

    # PM
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    # [0, 1]-PM
    left_t = left_t / (2 * C) + 0.5
    right_t = right_t / (2 * C) + 0.5
    left_t = in_machine_error(left_t, 0)
    right_t = in_machine_error(right_t, 1)
    left_right_probability = left_right_probability * (2 * C)
    center_probability = center_probability * (2 * C)

    interval_endpoint = [0, left_t, right_t, 1]
    interval_probability = [left_right_probability, center_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint


def PM_on_C(epsilon, input_x):
    assert (-1 <= input_x <= 1)
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)

    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    interval_endpoint = [-C, left_t, right_t, C]
    interval_probability = [left_right_probability, center_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint


if __name__ == "__main__":
    # x = np.linspace(0, 1, 10, endpoint=False)
    x = [0, 0.1]
    for i, _ in enumerate(x):
        interval_probability, interval_endpoint = PM_on_01(1, x[i])
        distance = l1_distance(interval_probability, interval_endpoint, x[i], 3)
        print(f"L_1 distance: {distance}")
