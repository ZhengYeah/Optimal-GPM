import math
from src.min_error_mechanism import MinL1Mechanism
from src.utilities import endpoints_to_lengths

epsilon = 1

piece_i = MinL1Mechanism(endpoint_a=0, endpoint_b=6.28, epsilon=epsilon, total_piece=3)
piece_i.solve_probabilities()
print(f"Probability list: {piece_i.probabilities}")
l_list = piece_i.solve_lr(3.14)[0]
error = piece_i.solve_lr(3.14)[1]
print("========")
print("Ground truth")
print("========")
print(f"Interval list: {l_list}")
print(f"Interval length list: {endpoints_to_lengths(l_list)}")
print(f"L1 error: {error}")

print("========")
print("Closed-form")
print("========")

x = 0
p = math.exp(epsilon / 2) / 6.28
tmp = 3.14 * (math.exp(0.5) - 1) / (math.exp(1) - 1)
l = x - tmp
r = x + tmp
print(f"p = {p}, l = {l / 3.14} * pi, r = {r / 3.14} * pi")
