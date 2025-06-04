import numpy as np
import pandas as pd
import pathlib
import sys
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1])) # Adjust the path to include the src directory
from src.closed_form_mechanism import classical_mechanism_01, unbias_gpm
from src.utilities import pdf_to_cdf, sampling_from_cdf
from src import PM, SW
# Set up the plotting environment
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 20
plt.rcParams['font.family'] = 'serif'

def compare_mechanisms(epsilon, data, n_bins):
    """
    one-round comparison
    :param data: [0,1] data array
    :param n_bins: number of bins
    """
    bins = np.linspace(0, 1, n_bins, endpoint=True)
    gt_hist, _ = np.histogram(data, bins=bins)

    acceleration_gpm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = classical_mechanism_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_gpm[i] = sampling_from_cdf(cdf, endpoints)
    gpm_hist, _ = np.histogram(acceleration_gpm, bins=bins)

    acceleration_pm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = PM.PM_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_pm[i] = sampling_from_cdf(cdf, endpoints)
    pm_hist, _ = np.histogram(acceleration_pm, bins=bins)

    acceleration_sw = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = SW.SW_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_sw[i] = sampling_from_cdf(cdf, endpoints)
    sw_hist, _ = np.histogram(acceleration_sw, bins=bins)

    return gt_hist, gpm_hist, pm_hist, sw_hist


from multiprocessing import Pool
def compare_mechanisms_mean(epsilon, data):
    """
    one-round comparison
    :param data: [0,1] data array
    """
    gt_mean = np.mean(data)

    # estimate mean (GPM)
    acceleration_gpm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = classical_mechanism_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_gpm[i] = sampling_from_cdf(cdf, endpoints)
    gpm_mean = np.mean(acceleration_gpm)

    # estimate mean (unbias GPM)
    acceleration_unbias_gpm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = unbias_gpm(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_unbias_gpm[i] = sampling_from_cdf(cdf, endpoints)
    unbias_gpm_mean = np.mean(acceleration_unbias_gpm)

    # estimate mean (PM)
    acceleration_pm = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = PM.PM_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_pm[i] = sampling_from_cdf(cdf, endpoints)
    pm_mean = np.mean(acceleration_pm)

    # estimate mean (SW)
    acceleration_sw = np.zeros(len(data))
    for i, acce_value in enumerate(data):
        p, endpoints = SW.SW_on_01(epsilon, acce_value)
        cdf = pdf_to_cdf(p, endpoints)
        acceleration_sw[i] = sampling_from_cdf(cdf, endpoints)
    sw_mean = np.mean(acceleration_sw)

    return gt_mean, gpm_mean, unbias_gpm_mean, pm_mean, sw_mean

if __name__ == '__main__':
    epsilon_list = np.linspace(1, 8, 8, endpoint=True)
    n_bins = 50
    test_times = 50

    # read data form csv
    data_1 = pd.read_csv('../experiments/experimental/motion_sense_dws_1/sub_1.csv')
    data_2 = pd.read_csv('../experiments/experimental/motion_sense_dws_1/sub_2.csv')
    data_3 = pd.read_csv('../experiments/experimental/motion_sense_dws_1/sub_3.csv')
    data = pd.concat([data_1, data_2, data_3])

    acceleration = data['userAcceleration.x']
    acceleration = acceleration.values
    # normalize to [0, 1]
    acceleration = (acceleration - min(acceleration)) / (max(acceleration) - min(acceleration))

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

    plt.figure(figsize=(5, 4))
    plt.plot(epsilon_list, results_epsilon[:, 1], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 0], marker='+', markersize=8)
    plt.plot(epsilon_list, results_epsilon[:, 2], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 1])
    plt.plot(epsilon_list, results_epsilon[:, 0], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
    plt.xlabel(r'Privacy parameter $\varepsilon$')
    plt.ylabel(r'Distribution estimation error')
    plt.xticks(np.arange(1, 9, 1))
    plt.legend(loc='upper right')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(2, 2))

    ######## End of Figure 16a ########

    epsilon_list = np.linspace(1, 8, 8, endpoint=True)
    test_times = 50
    # results (NOTICE: 5 results in total)
    results_epsilon = np.zeros((len(epsilon_list), 5))
    for i, epsilon in enumerate(epsilon_list):
        print(f"epsilon: {epsilon} (parallel processing)")
        # parallel processing
        pool = Pool(processes=8)
        results = pool.starmap(compare_mechanisms_mean, [(epsilon, acceleration)] * test_times)
        results = np.array(results)
        results_epsilon[i] = np.mean(results, axis=0)
    # calculate error
    error = np.abs(results_epsilon - results_epsilon[:, 0].reshape(-1, 1))

    plt.figure(figsize=(5, 4))
    plt.plot(epsilon_list, error[:, 3], label='PM-C', linewidth=2, linestyle='-', color=[0, 0, 1], marker='+', markersize=8)
    plt.plot(epsilon_list, error[:, 4], label='SW-C', linewidth=2, linestyle='--', color=[0, 0, 0])
    plt.plot(epsilon_list, error[:, 1], label='OGPM', linewidth=2, linestyle='-', color=[1, 0, 0])
    plt.plot(epsilon_list, error[:, 2], label='Unbias OGPM', linewidth=2, linestyle='--', color=[1, 0, 1])
    plt.xlabel(r'Privacy parameter $\varepsilon$')
    plt.ylabel(r'Mean estimation error')
    plt.ylim(0, 0.1)
    plt.xticks(np.arange(1, 9, 1))
    # plt.yticks(np.arange(0, 0.1, 0.02))
    leg = plt.legend(loc='upper right')
    plt.show()

######## End of Figure 17a ########