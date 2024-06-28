import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.closed_form_mechanism import circular_mechanism_pi
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW, PM
pi = 3.14


def compare_mechanisms(epsilon, steering, n_bins):
    """
    one-round comparison
    :param steering: [0,2*pi] data array
    :param n_bins: number of bins
    """
    bins = np.linspace(0, 2 * pi, n_bins, endpoint=True)
    gt_hist, _ = np.histogram(steering, bins=bins)

    # estimate distribution (GPM)
    p, endpoints = circular_mechanism_pi(epsilon)  # p and endpoints at pi
    cdf = pdf_to_cdf(p, endpoints)
    steering_gpm = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        bias = pi - angle
        sample = sampling_from_cdf(cdf, endpoints)
        steering_gpm[i] = (sample - bias + np.finfo(float).eps) % (2 * pi)
    gpm_hist, _ = np.histogram(steering_gpm, bins=bins)

    # estimate distribution (PM)
    steering_pm = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        p, endpoints = PM.PM_on_D(0, 2 * pi, epsilon, angle)
        cdf = pdf_to_cdf(p, endpoints)
        sample = sampling_from_cdf(cdf, endpoints)
        steering_pm[i] = sample
    pm_hist, _ = np.histogram(steering_pm, bins=bins)

    # estimate distribution (SW)
    steering_sw = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        p, endpoints = SW.SW_on_D(0, 2 * pi, epsilon, angle)
        cdf = pdf_to_cdf(p, endpoints)
        sample = sampling_from_cdf(cdf, endpoints)
        steering_sw[i] = sample
    sw_hist, _ = np.histogram(steering_sw, bins=bins)

    return gt_hist, gpm_hist, pm_hist, sw_hist


if __name__ == '__main__':
    epsilon_list = np.linspace(1, 8, 15, endpoint=True)
    n_bins = 50
    test_times = 2000

    # read data form csv
    data_1 = pd.read_csv('motion_sense_dws_1/sub_1.csv')
    data_2 = pd.read_csv('motion_sense_dws_1/sub_2.csv')
    data_3 = pd.read_csv('motion_sense_dws_1/sub_3.csv')
    data = pd.concat([data_1, data_2, data_3])
    steering = data['attitude.roll']
    steering = steering.values
    print(f"Length of steering: {len(steering)}")
    print(f"Max steering: {max(steering)}, Min steering: {min(steering)}")

    # map steering angles to unit circle
    steering = steering % (2 * pi)
    # plot histogram
    plt.hist(steering, bins=50)
    plt.show()

    error_epsilon = np.zeros((len(epsilon_list), 4))
    for i, epsilon in enumerate(epsilon_list):
        print(f"epsilon: {epsilon}")

        # calculate histogram
        error_array = np.zeros((test_times, 3))
        for j in range(test_times):
            gt_hist, gpm_hist, pm_hist, sw_hist = compare_mechanisms(epsilon, steering, n_bins)
            error_array[j, 0] = np.linalg.norm(gt_hist - gpm_hist)
            error_array[j, 1] = np.linalg.norm(gt_hist - pm_hist)
            error_array[j, 2] = np.linalg.norm(gt_hist - sw_hist)
        # calculate mean error
        gpm_error = np.mean(error_array[:, 0])
        pm_error = np.mean(error_array[:, 1])
        sw_error = np.mean(error_array[:, 2])
        error_epsilon[i] = [epsilon, gpm_error, pm_error, sw_error]

    # save to csv
    error_epsilon_df = pd.DataFrame(error_epsilon, columns=['Epsilon', 'GPM', 'PM', 'SW'])
    error_epsilon_df.to_csv('distribution_circular.csv', index=False)
