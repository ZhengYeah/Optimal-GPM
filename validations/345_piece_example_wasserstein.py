from min_error_mechanism import MinWassersteinMechanism


for i in range(3, 6):
    piece_i = MinWassersteinMechanism(endpoint_a=0, endpoint_b=1, epsilon=1, total_piece=i)
    print(f"Piece number = {i}")
    piece_i.solve_probabilities()
    print(f"Probability List: {piece_i.probabilities}")
    l_list = piece_i.solve_lr(0.3)[0]
    print(f"Interval Lengths List: {l_list}")
