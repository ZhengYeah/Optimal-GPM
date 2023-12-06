import numpy as np


def l1_distance(p, l, x, total_piece):
    """
    :param p: probability list
    :param l: interval end-point of piece i
    :param x: true data
    :param total_piece: total piece
    :return: L_1 distance
    """
    mid = (total_piece - 1) // 2
    assert (0 <= x <= 1)
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
