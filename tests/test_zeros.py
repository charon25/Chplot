import logging
logging.disable(logging.CRITICAL)
import math
import unittest

from chplot.plot.utils import ZerosList
from chplot.plot.plot import _generate_graphs, _generate_inputs
from chplot.plot.plot_parameters import set_default_values
from chplot.plot.zeros import _compute_zeros
from mock_parameters import MockParameters


class TestComputeZeros(unittest.TestCase):

    # A list of zeros contains float 2-tuples either of the form (lower, upper) if the function is zero on an interval
    # or (x_zero, None) if the function is zero only at one point
    def assertZerosListAlmostEqual(self, computed_zeros: ZerosList, real_zeros: ZerosList):
        for (computed_lower, computed_upper), (real_lower, real_upper) in zip(computed_zeros, real_zeros):
            self.assertAlmostEqual(computed_lower, real_lower)
            self.assertAlmostEqual(computed_upper, real_upper)

    def test_no_zeros(self):
        parameters = MockParameters(expressions=['x'], x_lim=(1, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [])

    def test_one_simple_zero(self):
        parameters = MockParameters(expressions=['x'], x_lim=(-1, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, None)])

    def test_one_simple_zero_beginning(self):
        parameters = MockParameters(expressions=['x'], x_lim=(0, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, None)])

    def test_one_simple_zero_end(self):
        parameters = MockParameters(expressions=['x'], x_lim=(-2, 0))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, None)])

    def test_one_simple_float_zero(self):
        parameters = MockParameters(expressions=['x^2 - 2'], x_lim=(0, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(math.sqrt(2), None)])

    def test_multiple_simple_zeros(self):
        parameters = MockParameters(expressions=['(x + 2) * x * (x - 2)'], x_lim=(-3, 3))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(-2.0, None), (0.0, None), (2.0, None)])

    def test_multiple_tangent_zero(self):
        parameters = MockParameters(expressions=['x * x'], x_lim=(-1, 1))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, None)])

    def test_multiple_small_zeros(self):
        parameters = MockParameters(expressions=['x * x - 10^(-20)'], x_lim=(-1, 1))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(-1e-10, None), (1e-10, None)])

    def test_one_zero_interval(self):
        parameters = MockParameters(expressions=['1-rect(x)'], x_lim=(-2, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(-0.5, 0.5)])

    def test_one_zero_interval_one_simple_zero(self):
        parameters = MockParameters(expressions=['ifn(x, x, ifn(x - 1, 0, ifn(x - 2, x - 1, 3 - x)))'], x_lim=(-1, 4))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, 1.0), (3.0, None)])

    def test_one_zero_interval_beginning(self):
        parameters = MockParameters(expressions=['1-rect(x - 0.5)'], x_lim=(0, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, 1.0)])

    def test_one_zero_interval_end(self):
        parameters = MockParameters(expressions=['1-rect(x - 0.5)'], x_lim=(-1, 1))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertZerosListAlmostEqual(_compute_zeros(parameters, inputs, graph), [(0.0, 1.0)])

