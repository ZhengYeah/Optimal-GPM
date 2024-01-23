import numpy as np
from src.utilities import endpoints_to_lengths


def l1_distance(endpoint_a, endpoint_b, total_piece, p, l, x):
    """
    distance = |y - x|
    :param endpoint_a: start point of domain D
    :param endpoint_b: end point of domain D
    :param p: probability list
    :param l: interval endpoint list
    :param x: true data (private data)
    :param total_piece: piece number
    :return: distance (error)
    """
    mid = (total_piece - 1) // 2
    assert endpoint_a <= x <= endpoint_b
    assert (l[mid] <= x <= l[mid + 1])
    assert (len(p) + 1 == len(l))

    obj_tmp = np.zeros(total_piece)
    for i in range(total_piece):
        obj_tmp[i] = l[i + 1] * l[i + 1] - l[i] * l[i]
    obj_center = l[mid] * l[mid] + l[mid + 1] * l[mid + 1]

    left_distance = sum(x * p[i] * (l[i + 1] - l[i]) - obj_tmp[i] / 2 * p[i] for i in range(mid))
    right_distance = sum(obj_tmp[i] / 2 * p[i] - x * p[i] * (l[i + 1] - l[i]) for i in range(mid + 1, total_piece))

    res = (left_distance + right_distance +
           x * x * p[mid] - x * p[mid] * l[mid] - p[mid] * x * l[mid + 1] +
           obj_center / 2 * p[mid])
    return res


def wasserstein_distance(endpoint_a, endpoint_b, total_piece, p, l, x):
    """
    distance = |\int_{a}^{y} f_1(t) dt - \int_{a}^{y} f_2(t) dt|
    :param endpoint_a: start point of domain D
    :param endpoint_b: end point of domain D
    :param p: probability list
    :param l: interval endpoint list
    :param x: true data (private data)
    :param total_piece: piece number
    :return: distance (error)
    """
    assert endpoint_a <= x <= endpoint_b

    # endpoint list to length list
    assert len(l) == total_piece + 1
    l = endpoints_to_lengths(l)

    mid = (total_piece - 1) // 2
    assert (sum(l[i] for i in range(mid)) <= x - endpoint_a <= sum(l[i] for i in range(mid + 1)))
    assert (len(p) == len(l))

    # Encoding for CDF block height
    height = np.zeros(total_piece)
    for i in range(total_piece):
        height[i] = height[i - 1] + p[i] * l[i] if i > 0 else p[i] * l[i]

    # Encoding for integration of CDF
    left_integration = np.zeros(mid + 1)
    right_integration = np.zeros(mid + 1)
    left_length_x = x - endpoint_a - sum(l[i] for i in range(mid))
    height_x = left_length_x * p[mid]

    for i in range(mid + 1):
        if i == 0:
            left_integration[i] = height[i] * l[i] / 2
        elif i < mid:
            left_integration[i] = (height[i] + height[i - 1]) * l[i] / 2
        elif i == mid:
            left_integration[i] = left_length_x * (2 * height[i - 1] + height_x) / 2
    for i in range(mid + 1):
        if i == 0:
            right_integration[i] = (l[mid] - left_length_x) * (height[mid] + height_x) / 2
        else:
            right_integration[i] = (height[i + mid] + height[i + mid - 1]) * l[i + mid] / 2

    res = sum(left_integration) + (endpoint_b - endpoint_a - x) - sum(right_integration)
    return res


def l2_distance(endpoint_a, endpoint_b, total_piece, p, l, x):
    """
    distance = (y - x)^2
    :param endpoint_a: start point of domain D
    :param endpoint_b: end point of domain D
    :param p: probability list
    :param l: interval endpoint list
    :param x: true data (private data)
    :param total_piece: piece number
    :return: distance (error)
    """
    mid = (total_piece - 1) // 2
    assert endpoint_a <= x <= endpoint_b
    assert (l[mid] <= x <= l[mid + 1])
    assert (len(p) + 1 == len(l))

    obj_tmp = np.zeros(total_piece + 1)
    for i in range(total_piece):
        obj_tmp[i] = (l[i + 1] - x) ** 3 - (l[i] - x) ** 3

    res = sum(obj_tmp[i] * p[i] * (1 / 3) for i in range(total_piece))
    return res
