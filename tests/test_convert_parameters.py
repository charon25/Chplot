import logging
logging.disable(logging.CRITICAL)
import math
import unittest

from chplot.plot.plot_parameters import convert_parameters_expression, set_default_values
from mock_parameters import MockParameters


class TestConvertParameters(unittest.TestCase):

    # XLIM
    def test_xlim_int(self):
        parameters = MockParameters(x_lim=(0, 1))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.x_lim[0], 0.0)
        self.assertAlmostEqual(parameters.x_lim[1], 1.0)

    def test_xlim_float(self):
        parameters = MockParameters(x_lim=(0.5, 1.2))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.x_lim[0], 0.5)
        self.assertAlmostEqual(parameters.x_lim[1], 1.2)

    def test_xlim_float_str(self):
        parameters = MockParameters(x_lim=("0", "1"))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.x_lim[0], 0.0)
        self.assertAlmostEqual(parameters.x_lim[1], 1.0)

    def test_xlim_expression(self):
        parameters = MockParameters(x_lim=("sqrt(2)", "pi + 1"))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.x_lim[0], math.sqrt(2))
        self.assertAlmostEqual(parameters.x_lim[1], math.pi + 1)

    def test_xlim_default(self):
        parameters = MockParameters(x_lim=("_unknown_function(1)", "_unknown_function(2)"))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.x_lim[0], 0.0)
        self.assertAlmostEqual(parameters.x_lim[1], 1.0)

    # YLIM
    def test_ylim_int(self):
        parameters = MockParameters(y_lim=(0, 1))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.y_lim[0], 0.0)
        self.assertAlmostEqual(parameters.y_lim[1], 1.0)

    def test_ylim_float(self):
        parameters = MockParameters(y_lim=(0.5, 1.2))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.y_lim[0], 0.5)
        self.assertAlmostEqual(parameters.y_lim[1], 1.2)

    def test_ylim_float_str(self):
        parameters = MockParameters(y_lim=("0", "1"))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.y_lim[0], 0.0)
        self.assertAlmostEqual(parameters.y_lim[1], 1.0)

    def test_ylim_expression(self):
        parameters = MockParameters(y_lim=("sqrt(2)", "pi + 1"))
        set_default_values(parameters)
        convert_parameters_expression(parameters)

        self.assertAlmostEqual(parameters.y_lim[0], math.sqrt(2))
        self.assertAlmostEqual(parameters.y_lim[1], math.pi + 1)

