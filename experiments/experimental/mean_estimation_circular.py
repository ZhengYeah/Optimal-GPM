import pandas as pd
import numpy as np
from src.closed_form_mechanism import classical_mechanism_01
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW
import matplotlib.pyplot as plt

epsilon = 0.01

# read data form csv
data = pd.read_csv('driving_log.csv')
steering = data['steering_angle']
steering = steering.values
print(f"Length of steering: {len(steering)}")

# map steering angles to [0,1]
steering = (steering + 1) / 2

# mean estimation (ground truth)
mean_gt = np.mean(steering)


# estimate distribution (GPM)
steering_gpm = np.zeros(len(steering))
for i, angle in enumerate(steering):
    p, endpoints = classical_mechanism_01(epsilon, angle)
    cdf = pdf_to_cdf(p, endpoints)
    sample = sampling_from_cdf(cdf, endpoints)
    steering_gpm[i] = sample
# mean estimation (GPM)
mean_gpm = np.mean(steering_gpm)

# estimate distribution (SW)
steering_sw = np.zeros(len(steering))
for i, angle in enumerate(steering):
    p, endpoints = SW.SW_on_D(0, 1, epsilon, angle)
    cdf = pdf_to_cdf(p, endpoints)
    sample = sampling_from_cdf(cdf, endpoints)
    steering_sw[i] = sample
# mean estimation (SW)
mean_sw = np.mean(steering_sw)

print(f"Ground truth mean: {mean_gt}, GPM mean: {mean_gpm}, SW mean: {mean_sw} ")
