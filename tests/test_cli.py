import logging
logging.disable(logging.CRITICAL)
import unittest

from chplot.convert_args import CONSTANT_DEFAULT_REGRESSION_KEYWORDS, retrieve_constants, retrieve_expressions
from chplot.convert_args import get_default_regression_expression, _get_monomial
from mock_parameters import MockParameters


def fpc(filename: str) -> str:
    return f'tests\\test_files\\constants\\{filename}.txt'

def fpe(filename: str) -> str:
    return f'tests\\test_files\\expressions\\{filename}.txt'


class TestRetrieveConstants(unittest.TestCase):
    """The tests should be run (python -m unittest discover tests) from the parent directory in order for the filepaths to be correct."""


    def test_no_constants(self):
        parameters = MockParameters(constants_arg=None)
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, [])

    def test_no_file_one_value(self):
        parameters = MockParameters(constants_arg=["x=1"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["x=1"])

    def test_no_file_three_values(self):
        parameters = MockParameters(constants_arg=["x=1", "y=2", "z=3"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["x=1", "y=2", "z=3"])

    def test_one_empty_file_no_value(self):
        parameters = MockParameters(constants_arg=[fpc("constants_empty")])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, [])

    def test_one_file_no_value(self):
        parameters = MockParameters(constants_arg=[fpc("constants_1")])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["a=1"])

    def test_two_files_no_value(self):
        parameters = MockParameters(constants_arg=[fpc("constants_1"), fpc("constants_3")])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["a=1", "b=2", "c=3", "d=4"])

    def test_two_files_three_values(self):
        parameters = MockParameters(constants_arg=["x=1", fpc("constants_1"), "y=2", fpc("constants_3"), "z=3"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["x=1", "a=1", "y=2", "b=2", "c=3", "d=4", "z=3"])


class TestRetrieveExpressions(unittest.TestCase):
    """The tests should be run (python -m unittest discover tests) from the parent directory in order for the filepaths to be correct."""


    def test_no_expressions(self):
        parameters = MockParameters(expressions=[])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, [])

    def test_no_file_one_value(self):
        parameters = MockParameters(expressions=["x"])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["x"])

    def test_no_file_three_values(self):
        parameters = MockParameters(expressions=["x", "x+1", "x+2"])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["x", "x+1", "x+2"])

    def test_one_empty_file_no_value(self):
        parameters = MockParameters(expressions=[fpe("expressions_empty")])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, [])

    def test_one_file_no_value(self):
        parameters = MockParameters(expressions=[fpe("expressions_1")])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["x*2"])

    def test_two_files_no_value(self):
        parameters = MockParameters(expressions=[fpe("expressions_1"), fpe("expressions_3")])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["x*2", "x*3", "x*4", "x*5"])

    def test_two_files_three_values(self):
        parameters = MockParameters(expressions=["x", fpe("expressions_1"), "x+1", fpe("expressions_3"), "x+2"])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["x", "x*2", "x+1", "x*3", "x*4", "x*5", "x+2"])

    def test_comments(self):
        parameters = MockParameters(expressions=[fpe("expressions_with_comments")])
        retrieve_expressions(parameters)
        self.assertListEqual(parameters.expressions, ["3x-1", "x+pi"])


class TestGetDefaultRegressionExpression(unittest.TestCase):

    def test_no_regression_expression(self):
        self.assertEqual(get_default_regression_expression(None), None)

    def test_regression_expression_no_default(self):
        self.assertEqual(get_default_regression_expression('_ra * x'), '_ra * x')

    def test_constant_default(self):
        for keyword, expression in CONSTANT_DEFAULT_REGRESSION_KEYWORDS.items():
            self.assertEqual(get_default_regression_expression(keyword), expression)

    def test_get_monomial(self):
        self.assertEqual(_get_monomial(0), '_ra0')
        self.assertEqual(_get_monomial(1), '_ra1 * x')
        self.assertEqual(_get_monomial(2), '_ra2 * x^2')
        self.assertEqual(_get_monomial(100), '_ra100 * x^100')

    def test_polynomial_regression_keyword(self):
        self.assertEqual(get_default_regression_expression('p1'), '_ra1 * x + _ra0')
        self.assertEqual(get_default_regression_expression('poly1'), '_ra1 * x + _ra0')
        self.assertEqual(get_default_regression_expression('polynomial1'), '_ra1 * x + _ra0')
        self.assertEqual(get_default_regression_expression('pnomial1'), 'pnomial1')

    def test_polynomial_regression_degree(self):
        self.assertEqual(get_default_regression_expression('poly0'), '_ra0')
        self.assertEqual(get_default_regression_expression('poly1'), '_ra1 * x + _ra0')
        self.assertEqual(get_default_regression_expression('poly5'), '_ra5 * x^5 + _ra4 * x^4 + _ra3 * x^3 + _ra2 * x^2 + _ra1 * x + _ra0')
