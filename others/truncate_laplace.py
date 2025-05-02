from scipy.stats import laplace
import numpy as np

exp = np.e
epsilon = 1

# pdf of truncated laplace at 0 with input = 0
lap_at_0 = 1/2
# pdf of truncated laplace at 0 with input = 1
lap_at_1 = laplace.cdf(-1, scale=1/epsilon)

ratio = lap_at_0 / lap_at_1
print(ratio)




