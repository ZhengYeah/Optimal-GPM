import math
import numpy as np
import csv


def extended_compressed_piecewise(epsilon, interval_left_a, interval_right_b, input_x):
    mapped_input_x = (input_x - (interval_right_b + interval_left_a) / 2) * 2 / (interval_right_b - interval_left_a)
    sampled_value = compressed_piecewise(epsilon, mapped_input_x) * (interval_right_b - interval_left_a) / 2 + (interval_left_a + interval_right_b) / 2
    return sampled_value

def extended_piecewise(epsilon, interval_left_a, interval_right_b, input_x):
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    C = C * (interval_right_b - interval_left_a) / 2 + (interval_left_a + interval_right_b) / 2
    # print(f"Output [-C, C] should be in [{-C}, {C}]")
    mapped_input_x = (input_x - (interval_right_b + interval_left_a) / 2) * 2 / (interval_right_b - interval_left_a)
    sampled_value = piecewise(epsilon, mapped_input_x) * (interval_right_b - interval_left_a) / 2 + (interval_left_a + interval_right_b) / 2
    return sampled_value

def compressed_piecewise(epsilon, input_x):
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probality = center_probability / math.exp(epsilon)
    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1

    left_t = left_t / C
    right_t = right_t / C
    left_right_probality = left_right_probality * C
    center_probability = center_probability * C

    cdf_array = np.zeros(3)
    cdf_array[0] = left_right_probality * (left_t + 1)
    cdf_array[1] = cdf_array[0] + center_probability * (right_t - left_t)
    cdf_array[2] = cdf_array[1] + left_right_probality * (1 - right_t)
    # print(f"CDF = {cdf_array}")
    
    random_tmp = np.random.rand()
    if random_tmp < cdf_array[0]:
        return np.random.uniform(-1, left_t)
    elif random_tmp < cdf_array[1]:
        return np.random.uniform(left_t, right_t)
    else:
        return np.random.uniform(right_t, 1)


def piecewise(epsilon, input_x):
    C = (math.exp(epsilon / 2) + 1) / (math.exp(epsilon / 2) - 1)
    center_probability = (math.exp(epsilon) - math.exp(epsilon / 2)) / (2 * math.exp(epsilon / 2) + 2)
    left_right_probality = center_probability / math.exp(epsilon)

    left_t = (C + 1) / 2 * input_x - (C - 1) / 2
    right_t = left_t + C - 1
    cdf_array = np.zeros(3)
    cdf_array[0] = left_right_probality * (left_t + C)
    cdf_array[1] = cdf_array[0] + center_probability * (right_t - left_t)
    cdf_array[2] = cdf_array[1] + left_right_probality * (C - right_t)
    # print(f"CDF = {cdf_array}")
    
    random_tmp = np.random.rand()
    if random_tmp < cdf_array[0]:
        return np.random.uniform(-C, left_t)
    elif random_tmp < cdf_array[1]:
        return np.random.uniform(left_t, right_t)
    else:
        return np.random.uniform(right_t, C)

def generete_csv_on_discretization(discretization_number, example_number):
    # parameters for PM
    a, b = 0, 1
    epsilon = 0.1

    fields = ["Index", "Original", "Perturbed"]
    filename = "PM_on_discretization.csv"
    with open(filename, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        input_x_set = np.zeros(discretization_number)
        for i in range(discretization_number):
            input_x_set[i] = a + (b - a) / discretization_number * i

        # output_y_set = np.zeros(shape=(example_number,3))
        # for i in range(example_number):
        #     output_y_set[i] = [int(i % discretization_number), input_x_set[i % discretization_number], extended_compressed_piecewise(epsilon, a, b, input_x_set[i % discretization_number])]
        #     csvwriter.writerow(output_y_set[i])

        same_label_batch = example_number / discretization_number
        for i in range(example_number):
            batch_index = int(i // same_label_batch)
            one_row = [i // same_label_batch, input_x_set[batch_index], extended_compressed_piecewise(epsilon, a, b, input_x_set[batch_index])]
            csvwriter.writerow(one_row)


if __name__ == "__main__":
    a, b = -1, 9
    epsilon = 0.1

    # experiment_num = 100
    # input_x_set = np.zeros(experiment_num)
    # output_y_set = np.zeros(experiment_num)
    # for i in range(experiment_num):
    #     input_x_set[i] = np.random.uniform(a, b)
    #     output_y_set[i] = extended_compressed_piecewise(epsilon, a, b, input_x_set[i])
    # print(f"Input Mean: {np.mean(input_x_set)}")
    # print(f"Ouput Mean: {np.mean(output_y_set)}, Ouput Max: {np.max(output_y_set)}, Output Min: {np.min(output_y_set)}")

    # generete_csv_on_discretization(20, 20000)

    # piecewise(epsilon, 0)
    # compressed_piecewise(5, 0)
    extended_compressed_piecewise(1, 0, 1, 0)
