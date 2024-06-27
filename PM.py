import math
import numpy as np
from src.distance_metric import l1_distance


def in_machine_error(result, expectation):
    if abs(result - expectation) <= 100 * np.finfo(float).eps:
        return expectation
    else:
        return result


def PM_on_D(endpoint_a, endpoint_b, epsilon, input_x):
    """
    [endpoint_a, endpoint_b) -> [endpoint_a, endpoint_b)
    """
    assert (endpoint_a <= input_x <= endpoint_b)
    D_len = endpoint_b - endpoint_a
    # input mapping to PM's [-1, 1], = (x - D_len / 2) / (D / 2)
    input_x = 2 * input_x / D_len - 1

    # [-C,C]-PM
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    # D-PM
    left_t = left_t * D_len / (2 * C) + (D_len / 2)
    right_t = right_t * D_len / (2 * C) + (D_len / 2)
    left_t = in_machine_error(left_t, endpoint_a)
    right_t = in_machine_error(right_t, endpoint_b)
    left_right_probability = left_right_probability * (2 * C) / D_len
    center_probability = center_probability * (2 * C) / D_len
    assert left_right_probability >= center_probability / math.exp(epsilon) - np.finfo(float).eps

    interval_endpoint = [endpoint_a, left_t, right_t, endpoint_b]
    interval_probability = [left_right_probability, center_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint


def PM_on_01(epsilon, input_x):
    """
    [0, 1) -> [0, 1)
    """
    assert (0 <= input_x <= 1)
    # input mapping
    input_x = (input_x - 0.5) * 2

    # [-C,C]-PM
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probability = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    # [0,1]-PM
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
    """
    [-1, 1) -> [-C, C)
    """
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
    x = np.linspace(0, 1, 10, endpoint=False)
    # x = [0, 0.1]
    for i, _ in enumerate(x):
        interval_probability, interval_endpoint = PM_on_01(1, x[i])
        interval_probability_2, interval_endpoint_2 = PM_on_D(0, 1, 1, x[i])
        distance = l1_distance(0, 1, 3, interval_probability, interval_endpoint, x[i])
        distance_2 = l1_distance(0, 1, 3, interval_probability_2, interval_endpoint_2, x[i])

        print(f"L_1 distance: {distance}")
        print(f"L_1 distance 2: {distance_2}")
