import logging
logging.disable(logging.CRITICAL)
from typing import Optional
import unittest

import numpy as np

from chplot.plot.plot import _generate_graphs, _generate_inputs
from chplot.plot.plot_parameters import convert_parameters_expression, set_default_values
from chplot.plot.derivative import _get_first_derivative, _get_second_derivative, _get_third_derivative
from chplot.plot.derivative import _get_fourth_derivative, _get_fifth_derivative, _get_sixth_derivative
from chplot.plot.derivative import _get_nth_derivative
from chplot.plot.derivative import _get_max_number_of_points, _resize_array, _get_size_reduction


class TestUtilityFunctions(unittest.TestCase):

    def test_get_max_number_of_points(self):
        points_numbers = [_get_max_number_of_points(n) for n in range(1, 10)]
        self.assertListEqual(points_numbers, [1_000_000, 500_000, 10_000, 1000, 100, 100, 50, 50, 50])

    def test_get_size_reduction(self):
        reductions = [_get_size_reduction(n) for n in range(1, 13)]
        self.assertListEqual(reductions, [4, 4, 4, 4, 5, 5, 9, 9, 9, 9, 10, 10])

    def test_resize_array_no_resizing(self):
        x = list(range(100))
        self.assertListEqual(_resize_array(x, 1000), x)
        self.assertListEqual(_resize_array(x, 100), x)

    def test_resize_array_half(self):
        x = list(range(100))
        self.assertListEqual(_resize_array(x, 50), list(range(0, 100, 2)))

    def test_resize_array_irregular(self):
        x = list(range(100))
        self.assertListEqual(_resize_array(x, 13), [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98])

N = 100

class TestGetDerivatives(unittest.TestCase):

    def assertListAlmostEqual(self, list1: list, list2: list, places: Optional[int] = None, delta: Optional[float] = None):
        self.assertEqual(len(list1), len(list2))
        for elem1, elem2 in zip(list1, list2):
            self.assertAlmostEqual(elem1, elem2, places=places, delta=delta)

    def test_first_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = x - 1

        self.assertListAlmostEqual(_get_first_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(1)), places=7)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=1), np.ones(N - 2 * _get_size_reduction(1)), places=7)

    def test_second_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = x**2 - 1

        self.assertListAlmostEqual(_get_second_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(2)) * 2, places=7)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=2), np.ones(N - 2 * _get_size_reduction(2)) * 2, places=7)

    def test_third_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = x**3 - 1

        self.assertListAlmostEqual(_get_third_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(3)) * 6, places=7)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=3), np.ones(N - 2 * _get_size_reduction(3)) * 6, places=7)

    def test_fourth_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = x**4 - 1

        self.assertListAlmostEqual(_get_fourth_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(4)) * 24, places=6)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=4), np.ones(N - 2 * _get_size_reduction(4)) * 24, places=6)

    def test_fifth_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = 0.1 * x**5 - 1

        self.assertListAlmostEqual(_get_fifth_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(5)) * 12.0, places=4)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=5), np.ones(N - 2 * _get_size_reduction(5)) * 12.0, places=4)

    def test_sixth_derivative_constant(self):
        x = np.linspace(0, 1, N, endpoint=False)
        y = 0.01 * x**6 - 1

        self.assertListAlmostEqual(_get_sixth_derivative(y, x[1] - x[0]), np.ones(N - 2 * _get_size_reduction(6)) * 7.20, delta=0.1)
        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=6), np.ones(N - 2 * _get_size_reduction(6)) * 7.20, delta=0.1)

    def test_seventh_derivative_constant(self):
        x = np.linspace(0, 1, 50, endpoint=False)
        y = 0.001 * x**7 - 1

        self.assertListAlmostEqual(_get_nth_derivative(y, x[1] - x[0], n=7), np.ones(50 - 2 * _get_size_reduction(7)) * 5.04, delta=0.1)
