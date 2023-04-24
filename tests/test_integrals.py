import logging
logging.disable(logging.CRITICAL)
import math
import unittest

from chplot.plot.plot import _generate_graphs, _generate_inputs, _load_functions
from chplot.plot.plot_parameters import convert_parameters_expression, set_default_values
from chplot.plot.integral import _compute_integral
from mock_parameters import MockParameters


class TestComputeIntegrals(unittest.TestCase):

    def assertTupleAlmostEqual(self, tuple1: tuple, tuple2: tuple):
        self.assertEqual(len(tuple1), len(tuple2))
        for elem1, elem2 in zip(tuple1, tuple2):
            self.assertAlmostEqual(elem1, elem2)

    def test_exact_integral_1(self):
        parameters = MockParameters(expressions=['x'], x_lim=(0, 1))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertAlmostEqual(_compute_integral(parameters, graph), 0.5)

    def test_exact_integral_2(self):
        parameters = MockParameters(expressions=['7*x-2'], x_lim=(-4, 3))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertAlmostEqual(_compute_integral(parameters, graph), -38.5)

    def test_integral_polynome(self):
        parameters = MockParameters(expressions=['3*x^3-2*x^2+x-10'], x_lim=(-2, 6))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral = _compute_integral(parameters, graph)

        self.assertAlmostEqual(integral, 2240 / 3, places=3)

    def test_integral_half_circle(self):
        parameters = MockParameters(expressions=['sqrt(1-x^2)'], x_lim=(-1, 1))
        set_default_values(parameters)
        _load_functions(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral = _compute_integral(parameters, graph)

        self.assertAlmostEqual(integral, math.pi / 2, places=3)

    def test_integral_inverse(self):
        parameters = MockParameters(expressions=['1/x'], x_lim=(1, 'e'))
        set_default_values(parameters)
        convert_parameters_expression(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral = _compute_integral(parameters, graph)

        self.assertAlmostEqual(integral, 1.0, places=3)

    def test_integral_discontinuity(self):
        parameters = MockParameters(expressions=['heaviside(x)'], x_lim=(-2, 2))
        set_default_values(parameters)
        _load_functions(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral = _compute_integral(parameters, graph)

        self.assertAlmostEqual(integral, 2.0, places=3)

    def test_integral_nan(self):
        parameters = MockParameters(expressions=['sqrt(abs(x) - 2)'], x_lim=(-4, 4))
        set_default_values(parameters)
        _load_functions(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral = _compute_integral(parameters, graph)

        self.assertAlmostEqual(integral, 8 * math.sqrt(2) / 3, places=3)
