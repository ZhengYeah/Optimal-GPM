import numpy as np
import pandas as pd
from src.min_error_mechanism import MinL1Mechanism


x = 0
epsilon_set = np.zeros(50)
p_set = np.zeros(50)
for i, epsilon in enumerate(np.linspace(1, 10, 50)):
    piece_i = MinL1Mechanism(endpoint_a=0, endpoint_b=1, epsilon=epsilon, total_piece=3)
    piece_i.solve_probabilities()
    p_set[i] = piece_i.probabilities[1]
    epsilon_set[i] = epsilon
# write into csv
df = pd.DataFrame({'epsilon': epsilon_set, 'p': p_set})
df.to_csv('p_set.csv', index=False)
