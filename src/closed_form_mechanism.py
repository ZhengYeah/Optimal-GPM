import math
pi = 3.14


def classical_mechanism_01(epsilon, x):
    assert 0 <= x <= 1
    C = (math.exp(epsilon/2) - 1) / 2 / (math.exp(epsilon) - 1)
    p = math.exp(epsilon/2)
    if 0 <= x < C:
        l, r = 0, 2 * C
    elif 1-C <= x <= 1:
        l, r = 1 - 2 * C, 1
    else:
        l, r = x - C, x + C
    # p and endpoints list
    p_list = [p/math.exp(epsilon), p, p/math.exp(epsilon)]
    length_list = [0, l, r, 1]
    return p_list, length_list


def circular_mechanism(epsilon, x):
    """
    this is not suitable for sampling due to l_mod and r_mod, use the next function instead
    """
    assert 0 <= x < 2 * pi
    p = 1 / (2 * pi) * math.exp(epsilon/2)
    l_mod = (x - pi * (math.exp(epsilon/2) - 1) / (math.exp(epsilon) - 1)) % (2 * pi)
    r_mod = (x + pi * (math.exp(epsilon/2) - 1) / (math.exp(epsilon) - 1)) % (2 * pi)
    return p, l_mod, r_mod


def circular_mechanism_pi(epsilon):
    p, l, r = circular_mechanism(epsilon, pi)
    p_list = [p/math.exp(epsilon), p, p/math.exp(epsilon)]
    endpoints = [0, l, r, 2*pi]
    return p_list, endpoints


def unbias_gpm(epsilon, x):
    """
    unbiased GPM mechanism (Theorem 5)
    """
    assert 0 <= x <= 1
    C = (math.exp(epsilon/2) + 1) / (math.exp(epsilon/2) - 1)
    p = math.exp(epsilon/2) / (2*C+1)
    l = (C+1) / 2 * x - (3*C+1)*(C-1) / (4*C)
    r = (C+1) / 2 * x + (C+1)*(C-1) / (4*C)
    # p and endpoints list
    p_list = [p/math.exp(epsilon), p, p/math.exp(epsilon)]
    length_list = [-C, l, r, 1+C]
    return p_list, length_list

