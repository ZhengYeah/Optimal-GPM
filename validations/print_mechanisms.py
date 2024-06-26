import SW, PM
from src.closed_form_mechanism import classical_mechanism_01
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


def print_distance(epsilon, input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    gpm_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    pm_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    sw_distance = l1_distance(0, 1, 3, p, endpoints, input_x)
    print(f"GPM Distance: {gpm_distance}")
    print(f"PM Distance: {pm_distance}")
    print(f"SW Distance: {sw_distance}")


if __name__ == '__main__':
    epsilon = 8
    input_x = 0.4
    print_mechanisms_01(epsilon, input_x)
    print_distance(epsilon, input_x)
