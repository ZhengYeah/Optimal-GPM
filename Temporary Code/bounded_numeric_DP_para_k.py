import math
import numpy as np
import csv


def bounded_numeric_dp(epsilon, interval_left_a, interval_right_b, input_x, m, k):
    if interval_left_a >= interval_right_b or input_x < interval_left_a or input_x > interval_right_b:
        raise ValueError("Check input bounds")
    R = interval_right_b - interval_left_a
    d_1, d_2 = input_x - interval_left_a, interval_right_b - input_x

    if d_1 == d_2:
        sampled_value = sample_on_cdf_1(R, epsilon, m)
    elif d_1 < d_2:
        sampled_value = sample_on_cdf_2(R, d_1, epsilon, m, k)
    else:
        sampled_value = sample_on_cdf_3(R, d_2, epsilon, m, k)
    return interval_left_a + sampled_value


def sample_on_cdf_1(R, epsilon, m):
    probability_1 = 2 / (math.exp(epsilon) + 1) / R
    delta = (math.exp(epsilon) - 1) / (m / 2 - 1) * probability_1

    pdf_array = np.zeros(m)
    pdf_array[0] = probability_1
    for i in range(1, m // 2):
        pdf_array[i] = probability_1 + i * delta
    for i in range(m // 2, m):
        pdf_array[i] = pdf_array[m - i - 1]
    # print(f"Case 1 : PDF =")
    # print(f"{pdf_array}")
    cdf_array = np.zeros(m)
    cdf_array[0] = pdf_array[0] * R / m
    for i in range(1, m):
        cdf_array[i] = cdf_array[i - 1] + pdf_array[i] * R / m
    # print(f"Case 1: CDF(\infinity) = {cdf_array[-1]}")
    
    random_tmp = np.random.rand()
    interval_ind = 0
    for i, cdf in enumerate(cdf_array):
        if random_tmp <= cdf:
            interval_ind = i
            break
    return np.random.uniform(R * interval_ind / m, R * (interval_ind + 1) / m)

def sample_on_cdf_2(R, d_1, epsilon, m, k):
    if m - 2 * k < 0:
        raise ValueError("2 * k must be smaller than m")
    d_2 = R - d_1
    G = 2 * d_1 * (m - 2 * k) + d_1 * (k - 1) + (d_2 - d_1) * (m - 2 * k - 1) / 2
    probability_m = (m - k - 1) / (G * (math.exp(epsilon) - 1) + (m - k - 1) * (d_1 + d_2))
    delta = (math.exp(epsilon) - 1) / (m - k - 1) * probability_m
    pdf_array = np.zeros(m)
    for i in range(k, m):
        pdf_array[i] = probability_m + (m - i - 1) * delta
    for i in range(k):
        pdf_array[i] = probability_m + (m - 2 * k + i) * delta
    # print(f"Case 2: PDF =")
    # print(f"{pdf_array}")
    cdf_array = np.zeros(m)
    cdf_array[0] = pdf_array[0] * d_1 / k
    for i in range(1, 2 * k):
        cdf_array[i] = cdf_array[i - 1] + pdf_array[i] * d_1 / k
    for i in range(2 * k, m):
        cdf_array[i] = cdf_array[i - 1] + pdf_array[i] * (d_2 - d_1) / (m - 2 * k)
    # print(f"Case 2: CDF(\infinity) = {cdf_array[-1]}")
    
    random_tmp = np.random.rand()
    interval_ind = 0
    for i, cdf in enumerate(cdf_array):
        if random_tmp <= cdf:
            interval_ind = i
            break
    # Debug: sampling intervals 
    # for interval_ind in range(m):
    #     if interval_ind < 2 * k:
    #         print(f"Interval {interval_ind}: [{interval_ind * d_1 / k}, {(interval_ind + 1) * d_1 / k}]")
    #     else:
    #         interval_ind = interval_ind - 2 * k
    #         interval_size = (d_2 - d_1) / (m - 2 * k)
    #         print(f"Interval {interval_ind + 2 * k}: [{interval_ind * interval_size + 2 * d_1}, {(interval_ind + 1) * interval_size + 2 * d_1}]") 

    if interval_ind < 2 * k:
        return np.random.uniform(interval_ind * d_1 / k, (interval_ind + 1) * d_1 / k)
    else:
        interval_ind = interval_ind - 2 * k
        interval_size = (d_2 - d_1) / (m - 2 * k)
        return np.random.uniform(interval_ind * interval_size, (interval_ind + 1) * interval_size) + 2 * d_1

def sample_on_cdf_3(R, d_2, epsilon, m, k):
    if m - 2 * k < 0:
        raise ValueError("2 * k must be smaller than m")
    d_1 = R - d_2
    m_1 = m - 2 * k
    G = (R * (m_1 - 1) + d_2 * (m_1 + m)) / 2
    probability_1 = (m - k - 1) /( G * (math.exp(epsilon) - 1) + R * (m - k - 1))
    delta = (2 * (math.exp(epsilon) - 1)) / (m + m_1 - 2) * probability_1
    pdf_array = np.zeros(m)
    pdf_array[0] = probability_1
    for i in range(1, (m_1 + m) // 2):
        pdf_array[i] = probability_1 + i * delta
    for i in range(((m_1 + m) // 2), m):
        pdf_array[i] = probability_1 + (m + m_1 - i - 1) * delta
    # print(f"Case 3: PDF =")
    # print(f"{pdf_array}")
    cdf_array = np.zeros(m)
    cdf_array[0] = pdf_array[0] * (d_1 - d_2) / m_1
    for i in range(1, m_1):
        cdf_array[i] = cdf_array[i - 1] + pdf_array[i] * (d_1 - d_2) / m_1
    for i in range(m_1, m):
        cdf_array[i] = cdf_array[i - 1] + pdf_array[i] * (2 * d_2) / (m - m_1)
    # print(f"Case 3: CDF(\infinity) = {cdf_array[-1]}")
    
    random_tmp = np.random.rand()
    interval_ind = 0
    for i, cdf in enumerate(cdf_array):
        if random_tmp <= cdf:
            interval_ind = i
            break
    # Debug: sampling intervals
    # for interval_ind in range(m):
    #     if interval_ind < m_1:
    #         print(f"Interval {interval_ind}: [{interval_ind * (d_1 - d_2) / m_1}, {(interval_ind + 1) * (d_1 - d_2) / m_1}]")
    #     else:
    #         interval_ind = interval_ind - m_1
    #         interval_size = (2 * d_2) / (m - m_1)
    #         print(f"Interval {interval_ind + m_1}: [{interval_ind * interval_size + (d_1 - d_2)}, {(interval_ind + 1) * interval_size + (d_1 - d_2)}]")

    if interval_ind < m_1:
        return np.random.uniform(interval_ind * (d_1 - d_2) / m_1, (interval_ind + 1) * (d_1 - d_2) / m_1)
    else:
        interval_ind = interval_ind - m_1
        interval_size = 2 * d_2 / (m - m_1)
        return np.random.uniform(interval_ind * interval_size, (interval_ind + 1) * interval_size) + (d_1 - d_2)

# used for ML (deprecated)
def generete_csv_on_discretization(discretization_number, example_number):
    # parameters for BN-DP
    a, b = 0, 1
    m, k = 26, 10
    epsilon = 0.1

    fields = ["Index", "Original", "Perturbed"]
    filename = "BN_DP_on_discretization_test.csv"
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        input_x_set = np.zeros(discretization_number)
        for i in range(discretization_number):
            input_x_set[i] = a + (b - a) / discretization_number * i
        output_y_set = np.zeros(shape=(example_number,3))
        for i in range(example_number):
            output_y_set[i] = [int(i % discretization_number), input_x_set[i % discretization_number], bounded_numeric_dp(epsilon, a, b, input_x_set[i % discretization_number], m, k)]
            csvwriter.writerow(output_y_set[i])



if __name__ == "__main__":
    a, b = 0, 1
    m, k = 26, 10
    epsilon = 0.1

    experiment_num = 1000
    input_x_set = np.zeros(experiment_num)
    output_y_set = np.zeros(experiment_num)
    for i in range(experiment_num):
        input_x_set[i] = np.random.uniform(a, b)
        output_y_set[i] = bounded_numeric_dp(epsilon, a, b, input_x_set[i], m, k)
    print(f"Input Mean: {np.mean(input_x_set)}")
    print(f"Ouput Mean: {np.mean(output_y_set)}")


