import math
import numpy as np
from src.distance_metric import l1_distance, l2_distance


def in_machine_error(result, expectation):
    if abs(result - expectation) <= np.finfo(float).eps:
        return expectation
    else:
        return result


def SW_on_D(endpoint_a, endpoint_b, epsilon, input_x):
    assert (endpoint_a <= input_x <= endpoint_b)
    D_len = endpoint_b - endpoint_a

    # SW's [-b, 1+b]
    b = (epsilon * math.exp(epsilon) - math.exp(epsilon) + 1) / (2 * math.exp(epsilon) * (math.exp(epsilon) - 1 - epsilon))
    central_probability = math.exp(epsilon) / (2 * b * math.exp(epsilon) + 1)
    left_right_probability = 1 / (2 * b * math.exp(epsilon) + 1)

    # D-SW
    central_probability = central_probability * (1 + 2 * b) / D_len
    left_right_probability = left_right_probability * (1 + 2 * b) / D_len
    # 这里 domain 变换很容易出错，注意写 assertion 测试
    left_t = input_x * D_len / (1 + 2 * b) + endpoint_a
    right_t = (input_x + 2 * b) * D_len / (1 + 2 * b) + endpoint_a
    left_t = in_machine_error(left_t, endpoint_a)
    right_t = in_machine_error(right_t, endpoint_b)
    interval_endpoint = [endpoint_a, left_t, right_t, endpoint_b]
    interval_probability = [left_right_probability, central_probability, left_right_probability]
    # print(f"Interval endpoint: [{interval_endpoint}]")
    # print(f"Interval probability: [{interval_probability}]")
    return interval_probability, interval_endpoint

def SW_on_01(epsilon, input_x):
    assert (0 <= input_x <= 1)
    b = (epsilon * math.exp(epsilon) - math.exp(epsilon) + 1) / (2 * math.exp(epsilon) * (math.exp(epsilon) - 1 - epsilon))
    central_probability = math.exp(epsilon) / (2 * b * math.exp(epsilon) + 1)
    left_right_probability = 1 / (2 * b * math.exp(epsilon) + 1)

    central_probability = central_probability * (1 + 2 * b)
    left_right_probability = left_right_probability * (1 + 2 * b)
    left_t = input_x / (1 + 2 * b)
    right_t = (input_x + 2 * b) / (1 + 2 * b)
    left_t = in_machine_error(left_t, 0)
    right_t = in_machine_error(right_t, 1)
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
    # x = np.linspace(0, 1, 10, endpoint=False)
    x = [0.5]
    for i, _ in enumerate(x):
        interval_probability, interval_endpoint = SW_on_01(1, x[i])
        # interval_probability_2, interval_endpoint_2 = SW_on_D(0, 1, 1, x[i])
        distance = l1_distance(0, 1, 3, interval_probability, interval_endpoint, x[i])
        # distance_2 = l1_distance(0, 1, 3, interval_probability_2, interval_endpoint_2, x[i])
        print(interval_probability, interval_endpoint)

        # print(f"L_1 distance: {distance}")
        # print(f"L_1 distance 2: {distance_2}")

        # interval_probability_3, interval_endpoint_3 = SW(4, x[i])
        # distance_3 = l2_distance(0, 1, 3, interval_probability_3, interval_endpoint_3, x[i])
        # print(interval_probability_3, interval_endpoint_3)
        # print(f"L_1 distance: {distance_3}")

