import pandas as pd
import numpy as np
from multiprocessing import Pool
from src.closed_form_mechanism import classical_mechanism_01
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW, PM


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

    return gt_mean, gpm_mean, pm_mean, sw_mean


if __name__ == '__main__':
    epsilon_list = range(1, 8)
    test_times = 100

    # read data form csv
    data = pd.read_csv('./motion_sense_dws_1/sub_1.csv')
    acceleration = data['userAcceleration.x']
    acceleration = acceleration.values
    print(f"Length of acceleration: {len(acceleration)}")
    print(f"Max acceleration: {max(acceleration)}, Min acceleration: {min(acceleration)}")
    # normalize to [0, 1]
    acceleration = (acceleration - min(acceleration)) / (max(acceleration) - min(acceleration))
    results_epsilon = np.zeros((len(epsilon_list), 4))
    for i, epsilon in enumerate(epsilon_list):
        print(f"epsilon: {epsilon}")
        # parallel processing
        pool = Pool(processes=8)
        results = pool.starmap(compare_mechanisms, [(epsilon, acceleration)] * test_times)
        results = np.array(results)
        results_epsilon[i] = np.mean(results, axis=0)

    # save to csv
    np.savetxt('mean_classical_domain.csv', results_epsilon, delimiter=',')
