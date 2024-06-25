import pandas as pd
import numpy as np
from src.closed_form_mechanism import circular_mechanism_pi
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW

pi = 3.14
epsilon = 6

# read data form csv
data = pd.read_csv('driving_log.csv')
steering = data['steering_angle']
steering = steering.values
print(f"Length of steering: {len(steering)}")

# map steering angles to unit circle
steering = steering * pi
steering = steering % (2 * pi)

# mean estimation (ground truth)
gt_mean = np.mean(steering)


# estimate distribution (GPM)
p, endpoints = circular_mechanism_pi(epsilon)  # p and endpoints at pi
cdf = pdf_to_cdf(p, endpoints)
steering_gpm = np.zeros(len(steering))
for i, angle in enumerate(steering):
    bias = pi - angle
    sample = sampling_from_cdf(cdf, endpoints)
    steering_gpm[i] = (sample - bias + np.finfo(float).eps) % (2 * pi)
gpm_mean = np.mean(steering_gpm)


# estimate distribution (SW)
steering_sw = np.zeros(len(steering))
for i, angle in enumerate(steering):
    p, endpoints = SW.SW_on_D(0, 2*pi, epsilon, angle)
    cdf = pdf_to_cdf(p, endpoints)
    sample = sampling_from_cdf(cdf, endpoints)
    steering_sw[i] = sample
sw_mean = np.mean(steering_sw)

print(f"Ground truth mean: {gt_mean}, GPM mean: {gpm_mean}, SW mean: {sw_mean}")
