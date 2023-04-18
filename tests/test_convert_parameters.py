import logging
import os
import pathlib
import shutil
logging.disable(logging.CRITICAL)
import math
import unittest

from chplot.functions import FUNCTIONS
from chplot.functions.utils import FunctionDict
from chplot.plot.plot_parameters import convert_parameters_expression, retrieve_python_functions, set_default_values
from mock_parameters import MockParameters


class TestConvertParametersLimits(unittest.TestCase):

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

        self.assertIsNone(parameters.x_lim[0])
        self.assertIsNone(parameters.x_lim[1])

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

    def test_ylim_default(self):
        parameters = MockParameters(y_lim=("_unknown_function(1)", "_unknown_function(2)"))
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertIsNone(parameters.y_lim[0])
        self.assertIsNone(parameters.y_lim[1])


class TestConvertParametersConstants(unittest.TestCase):

    def assertFunctionDictContains(self, larger_dict: FunctionDict, sub_dict: FunctionDict) -> None:
        for key, (_, value) in sub_dict.items():
            self.assertTrue(key in larger_dict)
            if math.isnan(value):
                self.assertTrue(math.isnan(larger_dict[key][1]))
            else:
                self.assertAlmostEqual(larger_dict[key][1], value)

    def assertDictNotContains(self, larger_dict: dict, keys: list) -> None:
        for key in keys:
            self.assertFalse(key in larger_dict)


    def test_two_simple_constants(self):
        parameters = MockParameters(constants=['a=1', 'b=2'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertFunctionDictContains(FUNCTIONS, {'a': (0, 1.0), 'b': (0, 2.0)})

    def test_one_simple_constant_with_spaces(self):
        parameters = MockParameters(constants=['a   = 1  ', '  b  = 2 '])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertFunctionDictContains(FUNCTIONS, {'a': (0, 1.0), 'b': (0, 2.0)})

    def test_three_complex_constants(self):
        parameters = MockParameters(constants=['a=sqrt(2)+1', 'b=pi/2-4', 'c=1/(1+4/7)'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertFunctionDictContains(FUNCTIONS, {'a': (0, math.sqrt(2) + 1), 'b': (0, math.pi / 2 - 4), 'c': (0, 1 / (1 + 4 / 7))})

    def test_constants_with_parse_error(self):
        parameters = MockParameters(constants=['_new_constant_a', '_new_constant_b:1', '_new_constant_c=34=6'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertDictNotContains(FUNCTIONS, ['_new_constant_a', '_new_constant_b', '_new_constant_c'])

    def test_constants_with_compute_error(self):
        parameters = MockParameters(constants=['_new_constant_a=1+', '_new_constant_b=sin()'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertDictNotContains(FUNCTIONS, ['_new_constant_a', '_new_constant_b', '_new_constant_c'])

    def test_constant_equals_nan(self):
        parameters = MockParameters(constants=['a=1/0', 'b=zeta(1)'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertFunctionDictContains(FUNCTIONS, {'a': (0, math.nan), 'b': (0, math.nan)})

    def test_constant_successive_use(self):
        parameters = MockParameters(constants=['a=1', 'b=a*2', 'c=b+1'])
        set_default_values(parameters)

        convert_parameters_expression(parameters)

        self.assertFunctionDictContains(FUNCTIONS, {'a': (0, 1), 'b': (0, 2), 'c': (0, 3)})
