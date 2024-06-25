import numpy as np


def endpoints_to_lengths(endpoints):
    res = np.zeros(len(endpoints) - 1)
    for i in range(len(endpoints) - 1):
        res[i] = endpoints[i + 1] - endpoints[i]
    return res


def pdf_to_cdf(pdf, endpoints):
    assert len(pdf) == len(endpoints) - 1
    cdf = np.zeros(len(pdf))
    cdf[0] = pdf[0] * (endpoints[1] - endpoints[0])
    for i in range(1, len(pdf)):
        cdf[i] = cdf[i-1] + pdf[i] * (endpoints[i+1] - endpoints[i])
    return cdf


def sampling_from_cdf(cdf, endpoints):
    """
    output: sampled value from the distribution (start from the first endpoint)
    """
    assert len(cdf) == len(endpoints) - 1
    u = np.random.uniform(0, 1)
    for i in range(len(cdf)):
        if cdf[i] > u:
            return np.random.uniform(endpoints[i], endpoints[i+1])
    return np.random.uniform(endpoints[-1], endpoints[-1] + 1)
