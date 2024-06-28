import pandas as pd
import numpy as np
from src.closed_form_mechanism import classical_mechanism_01
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW, PM
import matplotlib.pyplot as plt


def compare_mechanisms(epsilon, data, n_bins):
    """
    one-round comparison
    :param data: [0,1] data array
    :param n_bins: number of bins
    """
    bins = np.linspace(0, 1, n_bins, endpoint=True)
    gt_hist, _ = np.histogram(data, bins=bins)
    # plt.bar(bins[:-1], gt_hist, width=1/n_bins, align='edge')
    # plt.show()

    acceleration_gpm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = classical_mechanism_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_gpm[i] = sampling_from_cdf(cdf, endpoints)
    gpm_hist, _ = np.histogram(acceleration_gpm, bins=bins)
    # plt.bar(bins[:-1], gpm_hist, width=1/n_bins, align='edge')
    # plt.show()

    acceleration_pm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = PM.PM_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_pm[i] = sampling_from_cdf(cdf, endpoints)
    pm_hist, _ = np.histogram(acceleration_pm, bins=bins)
    # plt.bar(bins[:-1], pm_hist, width=1/n_bins, align='edge')
    # plt.show()

    acceleration_sw = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = SW.SW_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_sw[i] = sampling_from_cdf(cdf, endpoints)
    sw_hist, _ = np.histogram(acceleration_sw, bins=bins)
    # plt.bar(bins[:-1], sw_hist, width=1/n_bins, align='edge')
    # plt.show()

    return gt_hist, gpm_hist, pm_hist, sw_hist


if __name__ == '__main__':
    epsilon_list = np.linspace(1, 8, 15, endpoint=True)
    n_bins = 50
    test_times = 500

    # read data form csv
    data_1 = pd.read_csv('./motion_sense_dws_1/sub_1.csv')
    data_2 = pd.read_csv('./motion_sense_dws_1/sub_2.csv')
    data_3 = pd.read_csv('./motion_sense_dws_1/sub_3.csv')
    data = pd.concat([data_1, data_2, data_3])

    acceleration = data['userAcceleration.x']
    acceleration = acceleration.values
    print(f"Length of acceleration: {len(acceleration)}")
    print(f"Max acceleration: {max(acceleration)}, Min acceleration: {min(acceleration)}")
    # normalize to [0, 1]
    acceleration = (acceleration - min(acceleration)) / (max(acceleration) - min(acceleration))
    # # plot histogram
    # bins = np.linspace(0, 1, n_bins, endpoint=True)
    # gt_hist, _ = np.histogram(acceleration, bins=bins)
    # plt.bar(bins[:-1], gt_hist, width=1/n_bins, align='edge')
    # plt.show()

    results_epsilon = np.zeros((len(epsilon_list), 3))
    for i, epsilon in enumerate(epsilon_list):
        print(f"epsilon: {epsilon}")

        # calculate histogram
        error_array = np.zeros((test_times, 3))
        for j in range(test_times):
            gt_hist, gpm_hist, pm_hist, sw_hist = compare_mechanisms(epsilon, acceleration, n_bins)
            # calculate error
            error_array[j, 0] = np.linalg.norm(gt_hist - gpm_hist)
            error_array[j, 1] = np.linalg.norm(gt_hist - pm_hist)
            error_array[j, 2] = np.linalg.norm(gt_hist - sw_hist)
        # calculate mean error
        gpm_error = error_array[:, 0]
        pm_error = error_array[:, 1]
        sw_error = error_array[:, 2]
        results_epsilon[i, 0] = np.mean(gpm_error)
        results_epsilon[i, 1] = np.mean(pm_error)
        results_epsilon[i, 2] = np.mean(sw_error)

    # save to csv
    results_epsilon = np.array(results_epsilon)
    epsilon_list = np.array(epsilon_list)
    assert results_epsilon.shape[0] == epsilon_list.shape[0]
    results = np.hstack((epsilon_list.reshape(-1, 1), results_epsilon))
    np.savetxt('distribution_classical.csv', results, delimiter=',', header='Epsilon,GPM,PM,SW', comments='')
