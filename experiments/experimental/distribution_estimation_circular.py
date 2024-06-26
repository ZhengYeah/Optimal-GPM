import pandas as pd
import numpy as np
from src.closed_form_mechanism import circular_mechanism_pi
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW
import matplotlib.pyplot as plt

pi = 3.14
epsilon = 6

# read data form csv
data = pd.read_csv('self_driving_car/driving_log.csv')
steering = data['steering_angle']
steering = steering.values
print(f"Length of steering: {len(steering)}")

# map steering angles to unit circle
steering = steering * pi
steering = steering % (2 * pi)
# create bins
n_bins = 100
bins = np.linspace(0, 2*pi, n_bins, endpoint=True)

# plot histogram (ground truth)
gt_hist, gt_bin_edges = np.histogram(steering, bins=bins)
plt.bar(bins[:-1], gt_hist, width=2*pi/n_bins, align='edge')
plt.show()


# estimate distribution (GPM)
p, endpoints = circular_mechanism_pi(epsilon)  # p and endpoints at pi
cdf = pdf_to_cdf(p, endpoints)
steering_gpm = np.zeros(len(steering))
for i, angle in enumerate(steering):
    bias = pi - angle
    sample = sampling_from_cdf(cdf, endpoints)
    steering_gpm[i] = (sample - bias + np.finfo(float).eps) % (2 * pi)
# plot histogram (noisy)
gpm_hist, _ = np.histogram(steering_gpm, bins=bins)
plt.bar(bins[:-1], gpm_hist, width=2*pi/n_bins, align='edge')
plt.show()

# estimate distribution (SW)
steering_sw = np.zeros(len(steering))
for i, angle in enumerate(steering):
    p, endpoints = SW.SW_on_D(0, 2*pi, epsilon, angle)
    cdf = pdf_to_cdf(p, endpoints)
    sample = sampling_from_cdf(cdf, endpoints)
    steering_sw[i] = sample
# plot histogram (noisy)
sw_hist, _ = np.histogram(steering_sw, bins=bins)
plt.bar(bins[:-1], sw_hist, width=2*pi/n_bins, align='edge')
plt.show()
