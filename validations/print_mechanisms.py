from src import PM, SW
from src.closed_form_mechanism import classical_mechanism_01, circular_mechanism_pi
from src.distance_metric import l1_distance


def print_mechanisms_01(epsilon, input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    print(f"classical_mechanism_01:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    print(f"PM_on_01:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    print(f"SW_on_01:")
    print(f"p = {p}, endpoints = {endpoints}")


def print_mechanisms_2pi(epsilon, input_x, endpoint_a=0, endpoint_b=2*3.14):
    p, endpoints = PM.PM_on_D(endpoint_a, endpoint_b, epsilon, input_x)
    print(f"PM_on_D:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = SW.SW_on_D(endpoint_a, endpoint_b, epsilon, input_x)
    print(f"SW_on_D:")
    print(f"p = {p}, endpoints = {endpoints}")
    p, endpoints = circular_mechanism_pi(epsilon)
    print(f"circular_mechanism_pi:")
    print(f"p = {p}, endpoints = {endpoints}")


def print_distance_01(epsilon, input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    gpm_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    pm_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    sw_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    print(f"GPM Distance: {gpm_distance}")
    print(f"PM Distance: {pm_distance}")
    print(f"SW Distance: {sw_distance}")


def print_pm_C(epsilon, input_x):
    p, endpoints = PM.PM_on_C(epsilon, input_x)
    print(f"PM_on_C:")
    print(f"p = {p}, endpoints = {endpoints}")



if __name__ == '__main__':
    epsilon = 1.32
    input_x = 1
    print_mechanisms_01(epsilon, input_x)
    print_distance_01(epsilon, input_x)

    print_mechanisms_2pi(epsilon, input_x)
