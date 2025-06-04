import pandas as pd
import numpy as np
from multiprocessing import Pool
from src.closed_form_mechanism import classical_mechanism_01, unbias_gpm
from src.utilities import pdf_to_cdf, sampling_from_cdf
from src import PM, SW


def compare_mechanisms(epsilon, data):
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
    # NOTICE: this outputs an enlarged domain, the error is not suitable for comparison
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
    epsilon_list = np.linspace(1, 8, 15, endpoint=True)
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
    # results (NOTICE: 5 results in total)
    results_epsilon = np.zeros((len(epsilon_list), 5))
    for i, epsilon in enumerate(epsilon_list):
        print(f"epsilon: {epsilon}")
        # parallel processing
        pool = Pool(processes=8)
        results = pool.starmap(compare_mechanisms, [(epsilon, acceleration)] * test_times)
        results = np.array(results)
        results_epsilon[i] = np.mean(results, axis=0)

    # calculate error
    error = np.abs(results_epsilon - results_epsilon[:, 0].reshape(-1, 1))
    # save to csv
    assert len(epsilon_list) == error.shape[0]
    epsilon_list = np.array(epsilon_list)
    error = np.concatenate([epsilon_list.reshape(-1, 1), error], axis=1)
    np.savetxt('mean_classical.csv', error, delimiter=',', header='Epsilon,GT,GPM,UB_GPM,PM,SW', comments='')
