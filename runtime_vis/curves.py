from typing import Callable, Any

import numpy as np


class Curve:
    def __init__(
        self,
        name: str,
        label: str,
        callable: Callable[[int, int, int], Any],
        color,
        initial_coefficient=1,
        initial_offset=1,
    ):
        self.name = name
        self.label = label
        self.callable = callable
        self.color = color
        self.initial_guess = [initial_coefficient, initial_offset]


def _curve_n(x, a, b):
    return a * x + b


def _curve_logn(x, a, b):
    return a * np.log(x) + b


def _curve_nlogn(x, a, b):
    return a * x * np.log(x) + b


def _curve_n2(x, a, b):
    return a * x ** 2 + b


def _curve_n3(x, a, b):
    return a * x ** 3 + b


def _curve_exponential(x, a, b):
    return a * 2 ** x + b


fit_n = Curve('n', 'n', _curve_n, 'gray')
fit_logn = Curve('logn', 'log n', _curve_logn, 'green')
fit_nlogn = Curve('nlogn', 'n log n', _curve_nlogn, 'blue')
fit_n2 = Curve('n2', 'n^2', _curve_n2, 'yellow')
fit_n3 = Curve('n3', 'n^3', _curve_n3, 'orange')
fit_exponential = Curve('2n', '2^n', _curve_exponential, 'red')

named_curves = {
    'n': fit_n,
    'logn': fit_logn,
    'nlogn': fit_nlogn,
    'n2': fit_n2,
    'n3': fit_n3,
    '2n': fit_exponential,
}
