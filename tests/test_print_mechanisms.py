import pytest
import numpy as np
import SW, PM
from src.closed_form_mechanism import classical_mechanism_01

epsilon = 1
input_x = 0.5

def test_SW_on_01(epsilon=epsilon, input_x=input_x):
    p, endpoints = SW.SW_on_01(epsilon, input_x)
    print(f"SW_on_01: p = {p}, endpoints = {endpoints}")


def test_PM_on_01(epsilon=epsilon, input_x=input_x):
    p, endpoints = PM.PM_on_01(epsilon, input_x)
    print(f"PM_on_01: p = {p}, endpoints = {endpoints}")


def test_classical_mechanism_01(epsilon=epsilon, input_x=input_x):
    p, endpoints = classical_mechanism_01(epsilon, input_x)
    print(f"classical_mechanism_01: p = {p}, endpoints = {endpoints}")
