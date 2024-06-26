import pandas as pd
import numpy as np
from src.closed_form_mechanism import classical_mechanism_01
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW, PM
import matplotlib.pyplot as plt

epsilon = 2
n_bins = 100

# read data form csv
data = pd.read_csv('./motion_sense_dws_1/sub_1.csv')
acceleration = data['userAcceleration.x']
acceleration = acceleration.values
print(f"Length of acceleration: {len(acceleration)}")
print(f"Max acceleration: {max(acceleration)}, Min acceleration: {min(acceleration)}")
# normalize to [0, 1]
acceleration = (acceleration - min(acceleration)) / (max(acceleration) - min(acceleration))


def compare_mechanisms(epsilon, data, n_bins):
    """
    one-round comparison
    :param data: [0,1] data array
    :param n_bins: number of bins
    """
    bins = np.linspace(0, 1, n_bins, endpoint=True)
    gt_hist, _ = np.histogram(data, bins=bins)
    plt.bar(bins[:-1], gt_hist, width=1/n_bins, align='edge')
    plt.show()

    acceleration_gpm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = classical_mechanism_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_gpm[i] = sampling_from_cdf(cdf, endpoints)
    gpm_hist, _ = np.histogram(acceleration_gpm, bins=bins)
    plt.bar(bins[:-1], gpm_hist, width=1/n_bins, align='edge')
    plt.show()

    acceleration_pm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = PM.PM_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_pm[i] = sampling_from_cdf(cdf, endpoints)
    pm_hist, _ = np.histogram(acceleration_pm, bins=bins)
    plt.bar(bins[:-1], pm_hist, width=1/n_bins, align='edge')
    plt.show()

    acceleration_sw = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = SW.SW_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_sw[i] = sampling_from_cdf(cdf, endpoints)
    sw_hist, _ = np.histogram(acceleration_sw, bins=bins)
    plt.bar(bins[:-1], sw_hist, width=1/n_bins, align='edge')
    plt.show()


