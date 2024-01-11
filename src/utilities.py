import numpy as np


def endpoints_to_lengths(endpoints):
    res = np.zeros(len(endpoints) - 1)
    for i in range(len(endpoints) - 1):
        res[i] = endpoints[i + 1] - endpoints[i]
    return res
