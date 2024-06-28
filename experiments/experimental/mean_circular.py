import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.closed_form_mechanism import circular_mechanism_pi
from src.utilities import pdf_to_cdf, sampling_from_cdf
import SW, PM
pi = 3.14


def circular_mean(angles):
    """
    Compute the circular mean of a set of angles
    :param angles: angles in radians
    :return: circular mean in radians
    """
    x = np.mean(np.cos(angles))
    y = np.mean(np.sin(angles))
    return np.arctan2(y, x)


def compare_mechanisms(epsilon, steering):
    """
    one-round comparison
    :param steering: [0,2*pi] data array
    """
    # mean estimation (ground truth)
    gt_mean = circular_mean(steering)

    # estimate distribution (GPM)
    p, endpoints = circular_mechanism_pi(epsilon)  # p and endpoints at pi
    cdf = pdf_to_cdf(p, endpoints)
    steering_gpm = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        bias = pi - angle
        sample = sampling_from_cdf(cdf, endpoints)
        steering_gpm[i] = (sample - bias + np.finfo(float).eps) % (2 * pi)
    # compute mean
    gpm_mean = circular_mean(steering_gpm)

    # estimate distribution (PM)
    steering_pm = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        p, endpoints = PM.PM_on_D(0, 2 * pi, epsilon, angle)
        cdf = pdf_to_cdf(p, endpoints)
        sample = sampling_from_cdf(cdf, endpoints)
        steering_pm[i] = sample
    pm_mean = circular_mean(steering_pm)

    # estimate distribution (SW)
    steering_sw = np.zeros(len(steering))
    for i, angle in enumerate(steering):
        p, endpoints = SW.SW_on_D(0, 2 * pi, epsilon, angle)
        cdf = pdf_to_cdf(p, endpoints)
        sample = sampling_from_cdf(cdf, endpoints)
        steering_sw[i] = sample
    sw_mean = circular_mean(steering_sw)

    return gt_mean, gpm_mean, pm_mean, sw_mean


if __name__ == '__main__':
    epsilon_list = np.linspace(1, 8, 15, endpoint=True)
    test_times = 500

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
        results = np.zeros((test_times, 4))
        for j in range(test_times):
            results[j] = compare_mechanisms(epsilon, steering)
        # compute errors
        errors_1 = np.abs(results - results[:, 0][:, None])
        errors_2 = np.abs(results - (2*pi-results[:, 0][:, None]))
        errors = np.minimum(errors_1, errors_2)
        mean_errors = np.mean(errors, axis=0)
        error_epsilon[i] = mean_errors
    # save results
    df = pd.DataFrame(epsilon_list, columns=['Epsilon'])
    df['GPM'] = error_epsilon[:, 1]
    df['PM'] = error_epsilon[:, 2]
    df['SW'] = error_epsilon[:, 3]
    df.to_csv('mean_circular.csv', index=False)
