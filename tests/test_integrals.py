import logging
logging.disable(logging.CRITICAL)
import math
import unittest

from chplot.plot.plot import _generate_graphs, _generate_inputs
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

        self.assertTupleAlmostEqual(_compute_integral(parameters, inputs, graph), (0.5, 0.0))

    def test_exact_integral_2(self):
        parameters = MockParameters(expressions=['7*x-2'], x_lim=(-4, 3))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]

        self.assertTupleAlmostEqual(_compute_integral(parameters, inputs, graph), (-38.5, 0.0))

    def test_integral_polynome(self):
        parameters = MockParameters(expressions=['3*x^3-2*x^2+x-10'], x_lim=(-2, 6))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral, abs_error = _compute_integral(parameters, inputs, graph)

        self.assertTrue(integral - abs_error <= 2240 / 3 <= integral + abs_error)

    def test_integral_half_circle(self):
        parameters = MockParameters(expressions=['sqrt(1-x^2)'], x_lim=(-1, 1))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral, abs_error = _compute_integral(parameters, inputs, graph)

        self.assertTrue(integral - abs_error <= math.pi / 2 <= integral + abs_error)

    def test_integral_inverse(self):
        parameters = MockParameters(expressions=['1/x'], x_lim=(1, 'e'))
        set_default_values(parameters)
        convert_parameters_expression(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral, abs_error = _compute_integral(parameters, inputs, graph)

        self.assertTrue(integral - abs_error <= 1.0 <= integral + abs_error)

    def test_integral_discontinuity(self):
        parameters = MockParameters(expressions=['heaviside(x)'], x_lim=(-2, 2))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral, abs_error = _compute_integral(parameters, inputs, graph)

        self.assertTrue(integral - abs_error <= 2.0 <= integral + abs_error)

    def test_integral_nan(self):
        parameters = MockParameters(expressions=['sqrt(abs(x) - 2)'], x_lim=(-4, 4))
        set_default_values(parameters)
        inputs = _generate_inputs(parameters)
        graph = _generate_graphs(parameters, inputs)[0]
        integral, abs_error = _compute_integral(parameters, inputs, graph)
        print(integral, abs_error)

        self.assertTrue(integral - abs_error <= 8 * math.sqrt(2) / 3 <= integral + abs_error)
