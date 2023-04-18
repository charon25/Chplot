import logging
logging.disable(logging.CRITICAL)
from typing import Union
import unittest

import numpy as np

from chplot.plot.regression import _get_unique_regression_parameters
from chplot.plot.regression import _check_regression_expression, compute_regressions
from chplot.plot.regression import  _get_fit_expression, _get_fit_rpn
from chplot.plot.utils import Graph, GraphType

from mock_parameters import MockParameters


class TestCheckRegressionExpression(unittest.TestCase):

    def test_correct_regression_expression(self):
        parameters = MockParameters(regression_expression='_ra * x', variable='x')
        self.assertEqual(_check_regression_expression(parameters), '_ra x *')

    def test_mismatched_brackets(self):
        parameters = MockParameters(regression_expression='(_ra * x', variable='x')
        self.assertIsNone(_check_regression_expression(parameters))

    def test_no_regression_parameters(self):
        parameters = MockParameters(regression_expression='x', variable='x')
        self.assertIsNone(_check_regression_expression(parameters))

        parameters = MockParameters(regression_expression='_r*x', variable='x')
        self.assertIsNone(_check_regression_expression(parameters))

    def test_invalid_regression_expression(self):
        parameters = MockParameters(regression_expression='_ra * _unknown_func(x)', variable='x')
        self.assertIsNone(_check_regression_expression(parameters))

        parameters = MockParameters(regression_expression='_ra * sin(x, 1)', variable='x')
        self.assertIsNone(_check_regression_expression(parameters))

    def test_overlapping_parameters(self):
        parameters = MockParameters(regression_expression='_ra * _rb', variable='x')
        self.assertIsNotNone(_check_regression_expression(parameters))


class TestGetUniqueRegressionParameters(unittest.TestCase):

    def test_get_simple(self):
        self.assertListEqual(_get_unique_regression_parameters('_ra'), ['_ra'])
        self.assertListEqual(_get_unique_regression_parameters('_ra 1 +'), ['_ra'])
        self.assertListEqual(_get_unique_regression_parameters('1 x + _ra sin *'), ['_ra'])

    def test_get_multiples(self):
        self.assertListEqual(_get_unique_regression_parameters('_ra x + _rb *'), ['_ra', '_rb'])

    def test_get_repeated(self):
        self.assertListEqual(_get_unique_regression_parameters('_ra x + _rb * _ra +'), ['_ra', '_rb'])

    def test_get_overlapping(self):
        self.assertListEqual(_get_unique_regression_parameters('_ra _rb *'), ['_ra', '_rb'])


class TestFitRPN(unittest.TestCase):

    def test_fit_rpn_base(self):
        rpn = 'x _ra * _rb +'
        self.assertEqual(_get_fit_rpn(rpn, ['_ra', '_rb'], ['1.5', '-0.3']), 'x 1.5 * -0.3 +')

    def test_fit_rpn_parameter_repeater(self):
        rpn = 'x _ra * _ra +'
        self.assertEqual(_get_fit_rpn(rpn, ['_ra'], ['1.5']), 'x 1.5 * 1.5 +')

    def test_fit_rpn_parameter_name_included_in_other(self):
        rpn = 'x _ra * _ra2 +'
        self.assertEqual(_get_fit_rpn(rpn, ['_ra', '_ra2'], ['1.5', '-0.3']), 'x 1.5 * -0.3 +')

    def test_fit_rpn_parameter_at_beginning_and_end(self):
        rpn = '_ra 1 +'
        self.assertEqual(_get_fit_rpn(rpn, ['_ra'], ['1.5']), '1.5 1 +')

        rpn = '_ra'
        self.assertEqual(_get_fit_rpn(rpn, ['_ra'], ['1.5']), '1.5')


class TestFitExpression(unittest.TestCase):

    def test_fit_expression_base(self):
        rpn = 'x * _ra + _rb'
        self.assertEqual(_get_fit_expression(rpn, ['_ra', '_rb'], ['1.5', '-0.3']), 'x * (1.5) + (-0.3)')

    def test_fit_expression_no_spaces(self):
        rpn = 'x*_ra+_rb'
        self.assertEqual(_get_fit_expression(rpn, ['_ra', '_rb'], ['1.5', '-0.3']), 'x*(1.5)+(-0.3)')

    def test_fit_expression_parameter_repeater(self):
        rpn = 'x * _ra + _ra'
        self.assertEqual(_get_fit_expression(rpn, ['_ra'], ['1.5']), 'x * (1.5) + (1.5)')

    def test_fit_expression_parameter_name_included_in_other(self):
        rpn = 'x * _ra + _ra2'
        self.assertEqual(_get_fit_expression(rpn, ['_ra', '_ra2'], ['1.5', '-0.3']), 'x * (1.5) + (-0.3)')

    def test_fit_expression_parameter_at_beginning_and_end(self):
        rpn = '_ra + x'
        self.assertEqual(_get_fit_expression(rpn, ['_ra'], ['1.5']), '(1.5) + x')

        rpn = 'x + _ra'
        self.assertEqual(_get_fit_expression(rpn, ['_ra'], ['1.5']), 'x + (1.5)')


class TestComputeRegression(unittest.TestCase):

    def assertRegressionGraphEqual(self, graph: Graph, inputs: Union[list[float], np.ndarray], expression: str, values: np.ndarray):
        self.assertEqual(graph.type, GraphType.REGRESSION)
        self.assertTrue(np.allclose(graph.inputs, inputs))
        self.assertEqual(graph.expression, expression)
        self.assertTrue(np.allclose(graph.values, values))


    def test_no_graphs(self):
        parameters = MockParameters(n_points=10, regression_expression='_ra * x', variable='x')
        self.assertListEqual(compute_regressions(parameters, []), [])

    def test_error_in_regression_expression(self):
        regression_expressions = ('(_ra * x', 'x', '_ra * _unknown_func(x)', '_ra * sin(x, 1)')
        for expression in regression_expressions:
            parameters = MockParameters(n_points=10, regression_expression=expression, variable='x')
            self.assertListEqual(compute_regressions(parameters, [Graph(None, None, None, None, None)]), [])

    def test_linear_regression_10_points(self):
        parameters = MockParameters(n_points=10, regression_expression='_ra * x', variable='x')

        inputs = np.linspace(1, 2, parameters.n_points)
        values = 3 * inputs
        graph = Graph(inputs=inputs, type=GraphType.BASE, expression='3x', rpn='3 x *', values=values)

        regression_graphs = compute_regressions(parameters, [graph])

        self.assertEqual(len(regression_graphs), 1)
        self.assertRegressionGraphEqual(regression_graphs[0], inputs, f'Regression [{graph.expression}]', values)

    def test_cubic_regression_1000_points(self):
        parameters = MockParameters(n_points=1000, regression_expression='_ra * x^3 + _rb * x^2 + _rc * x + _rd', variable='x')

        inputs = np.linspace(1, 2, parameters.n_points)
        values = 3 * inputs**3 - 2 * inputs**2 + inputs - 5
        graph = Graph(inputs=inputs, type=GraphType.BASE, expression='3x^3 - 2x^2 + x - 5', rpn='3 x 3 ^ * 2 x 2 ^ * - x + 5 -', values=values)

        regression_graphs = compute_regressions(parameters, [graph])

        self.assertEqual(len(regression_graphs), 1)
        self.assertRegressionGraphEqual(regression_graphs[0], inputs, f'Regression [{graph.expression}]', values)

    def test_two_regressions_different_xlim_n_points_values(self):
        parameters = MockParameters(n_points=10, regression_expression='_ra * x', variable='x')

        inputs1 = np.linspace(1, 2, parameters.n_points)
        values1 = 3 * inputs1
        graph1 = Graph(inputs=inputs1, type=GraphType.BASE, expression='3x', rpn='3 x *', values=values1)

        inputs2 = np.linspace(7, 8, parameters.n_points * 10)
        values2 = -8 * inputs2
        graph2 = Graph(inputs=inputs2, type=GraphType.BASE, expression='3x', rpn='3 x *', values=values2)

        regression_graphs = compute_regressions(parameters, [graph1, graph2])

        self.assertEqual(len(regression_graphs), 2)
        self.assertRegressionGraphEqual(regression_graphs[0], inputs1, f'Regression [{graph1.expression}]', values1)
        self.assertRegressionGraphEqual(regression_graphs[1], np.linspace(7, 8, parameters.n_points), f'Regression [{graph2.expression}]', -8 * np.linspace(7, 8, parameters.n_points))
