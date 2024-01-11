import math
from src.min_error_mechanism import MinL1CircleMechanism

for i in range(3, 4):
    piece_i = MinL1CircleMechanism(endpoint_a=0, endpoint_b=6.28, epsilon=1, total_piece=i)
    print(f"Piece number = {i}")
    piece_i.solve_probabilities()
    print(f"Probability List: {piece_i.probabilities}")
    l_list = piece_i.solve_lr(3.14)[0]
    print(f"Interval List: {l_list}")


p_epsilon = math.exp(0.5) / 6.28
l_x_epsilon = - (3.14 * math.exp(0.5) - 3.14) / (math.exp(1) - 1)
r_x_epsilon = (3.14 * math.exp(0.5) - 3.14) / (math.exp(1) - 1)

print(f"p_epsilon = {p_epsilon}")
print(f"l_x_epsilon = {l_x_epsilon}, r_x_epsilon = {r_x_epsilon}")
