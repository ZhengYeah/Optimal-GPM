from min_error_mechanism import MinL1Mechanism


for i in range(3, 6):
    piece_i = MinL1Mechanism(endpoint_a=0, endpoint_b=1, epsilon=1, total_piece=i)
    print(f"Piece number = {i}")
    piece_i.solve_probabilities()
    print(f"Probability List: {piece_i.probabilities}")
    l_list = piece_i.solve_lr(0.3)[0]
    lengths_list = piece_i.endpoints_to_lengths(l_list)
    print(f"Interval Lengths List: {lengths_list}")
