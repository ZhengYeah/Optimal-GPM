from src.min_error_mechanism import MinL1Mechanism
from src.utilities import endpoints_to_lengths


piece_i = MinL1Mechanism(endpoint_a=0, endpoint_b=6.28, epsilon=1, total_piece=3)
piece_i.solve_probabilities()
print(f"Probability List: {piece_i.probabilities}")
l_list = piece_i.solve_lr(1.57)[0]
error = piece_i.solve_lr(1.57)[1]
print(f"Interval Lengths List: {l_list}")
print(f"L1 error: {error}")

