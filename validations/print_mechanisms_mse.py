import numpy as np

import SW, PM
from src.closed_form_mechanism import classical_mechanism_01, circular_mechanism_pi
from src.distance_metric import l2_distance


def print_mechanisms_01(epsilon, input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    print(f"classical_mechanism_01:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    print(f"PM_on_01:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    print(f"SW_on_01:")
    print(f"p = {p}, endpoints = {endpoints}")


def print_mechanisms_2pi(epsilon, input_x, endpoint_a=0, endpoint_b=2*3.14):
    p, endpoints = PM.PM_on_D(endpoint_a, endpoint_b, epsilon, input_x)
    print(f"PM_on_D:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = SW.SW_on_D(endpoint_a, endpoint_b, epsilon, input_x)
    print(f"SW_on_D:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = circular_mechanism_pi(epsilon)
    print(f"circular_mechanism_pi:")
    print(f"p = {p}, endpoints = {endpoints}")


def print_distance_01(epsilon, input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    gpm_distance = l2_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    pm_distance = l2_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    sw_distance = l2_distance(0, 1, 3, p, endpoints, input_x)
    print(f"GPM Distance: {gpm_distance}")
    print(f"PM Distance: {pm_distance}")
    print(f"SW Distance: {sw_distance}")


if __name__ == '__main__':
    total = 10
    eps = np.linspace(0.01, total, 100, endpoint=False)

    mse = np.zeros(len(eps))
    for i, epsilon in enumerate(eps):
        p, endpoints = circular_mechanism_pi(epsilon)
        mse_circular = l2_distance(0, 2*3.14, 3, p, endpoints, 3.14)
        epsilon_2 = total - epsilon
        p, endpoints = classical_mechanism_01(total-epsilon, 0)
        mse_01 = l2_distance(0, 1, 3, p, endpoints, 0)
        mse[i] = mse_circular + mse_01
    # draw the plot
    import matplotlib.pyplot as plt
    plt.plot(eps, mse)
    plt.show()
    # print the minimum
    epsilon_argmin = eps[np.argmin(mse)]
    print(f"epsilon_argmin = {epsilon_argmin}")
    proportion = epsilon_argmin / total
    print(f"proportion = {proportion}")