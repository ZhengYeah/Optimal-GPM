import numpy as np


def wasserstein_distance(p, l, x, total_piece):
    """
    :param p: probability list
    :param l: interval lengths
    :param x: true data
    :param total_piece: total piece
    :return: L_1 distance
    """
    mid = (total_piece - 1) // 2
    assert (0 <= x <= 1)
    assert (sum(l[i] for i in range(mid)) <= x <= sum(l[i] for i in range(mid + 1)))
    assert (len(p) == len(l))

    # Encoding for CDF block height
    height = np.zeros(total_piece)
    for i in range(total_piece):
        height[i] = height[i - 1] + p[i] * l[i] if i > 0 else p[i] * l[i]

    # Encoding for integration of CDF
    left_integration = np.zeros(mid + 1)
    right_integration = np.zeros(mid + 1)
    left_length_x = x - sum(l[i] for i in range(mid))
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

    res = sum(left_integration) + (1 - x) - sum(right_integration)
    return res
