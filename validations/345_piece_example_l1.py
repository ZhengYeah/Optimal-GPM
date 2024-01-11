import math
from src.min_error_mechanism import MinL1Mechanism

x = 0.16
for i in range(3, 4):
    piece_i = MinL1Mechanism(endpoint_a=0, endpoint_b=1, epsilon=1, total_piece=i)
    print(f"Piece number = {i}")
    piece_i.solve_probabilities()
    print(f"Probability List: {piece_i.probabilities}")
    l_list = piece_i.solve_lr(x)[0]
    L1_error = piece_i.solve_lr(x)[1]
    lengths_list = piece_i.endpoints_to_lengths(l_list)
    print(f"Interval Lengths List: {lengths_list}")
    print(f"L1 error: {L1_error}")

    # ref for theorem 2
    print(math.exp(1 / 2))
    print((math.exp(0.5) - 1) / 2 / (math.exp(1) - 1))
