import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

data = pd.read_csv('p_set.csv')
X = data['epsilon'].values.reshape(-1, 1)
y = data['p'].values


def func(x, beta_1, beta_2):
    return np.exp(beta_1 * x) + beta_2

# Fit the model
popt, pcov = curve_fit(func, X.flatten(), y, p0=[1, 1.6483689986536187])
print(f"beta_1: {popt[0]}", f"beta_2: {popt[1]}")
print(f"pcov: {pcov}")
