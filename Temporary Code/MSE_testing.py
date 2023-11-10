import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

from bounded_numeric_DP_para_k import bounded_numeric_dp
from extended_piecewise import extended_compressed_piecewise


a, b = -1, 1
m, k = 4, 4
epsilon = 0.1

experiment_num = 1000
input_x_set = np.zeros(experiment_num)
output_y_set = np.zeros(experiment_num)
output_PM_set = np.zeros(experiment_num)
for i in range(experiment_num):
    input_x_set[i] = i
    output_y_set[i] = bounded_numeric_dp(epsilon, a, b, 0, m, k)
    output_PM_set[i] = extended_compressed_piecewise(epsilon, a, b, 0)
# print(f"Input Mean: {np.mean(input_x_set)}")
# print(f"Ouput Mean: {np.mean(output_y_set)}")
norm_PM = LA.norm(output_PM_set, 1)
norm_y = LA.norm(output_y_set, 1)
print(f"Norm of compressed PM: {norm_PM}")
print(f"Norm of Bounded Numeric DP: {norm_y}")


plt.scatter(input_x_set, output_PM_set)
plt.scatter(input_x_set, output_y_set)
plt.show()
