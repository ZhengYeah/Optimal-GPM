import numpy as np

exp = np.e
pi = np.pi


def mse_ogpm_0_C(epsilon, x=0):
    p_high = exp ** (epsilon / 2)
    p_low = p_high / (exp ** epsilon)
    C = (exp ** (epsilon / 2) - 1) / (exp ** epsilon - 1) / 2
    return p_high / 3 * ((2 * C - x) ** 3 + x ** 3) + p_low / 3 * (-(2 * C - x) ** 3 + (1 - x) ** 3)


def mse_ogpm_circular(epsilon):
    p_high = 1 / (2 * pi) * exp ** (epsilon / 2)
    p_low = p_high / (exp ** epsilon)
    C = (exp ** (epsilon / 2) - 1) / (exp ** epsilon - 1) * pi
    return 2 / 3 * (p_high * C ** 3 + p_low * (pi ** 3 - C ** 3))



if __name__ == "__main__":
    machine_delta = 0.01
    scope = 8
    epsilon = np.linspace(machine_delta,scope-machine_delta,100)
    mse_obj = mse_ogpm_0_C(epsilon) + mse_ogpm_circular(scope-epsilon)
    # draw the plot
    import matplotlib.pyplot as plt
    plt.plot(epsilon, mse_obj)
    plt.show()
    # print the minimum
    epsilon_argmin = epsilon[np.argmin(mse_obj)]
    proportion = epsilon_argmin / scope
    print(f"epsilon_argmin = {epsilon_argmin}, proportion = {proportion}")
    print(f"{1 / (1 + pi)}")


