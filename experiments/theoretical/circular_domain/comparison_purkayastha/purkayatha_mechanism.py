import numpy as np
import csv
from src.distance_metric import l2_distance
from src.min_error_mechanism import MinL2Mechanism


pi = np.pi
exp = np.e
epsilon = 2

# the expected surface distance between x \sim Pur(\mu, k) and the mode \mu, according to Theorem 22 in the following paper:
# paper name: Differential Privacy for Directional Data [CCS'21]
k = epsilon / pi
reminder = pi / (1 -exp ** (k * pi)) - 1 / k
# m = 1, so l has only one value 1
A_l = 1 / (k ** 2)
pur_error = 2 * k * A_l + reminder

print(f"Purkayastha error: {pur_error}")


