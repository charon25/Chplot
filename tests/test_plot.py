import logging
logging.disable(logging.CRITICAL)
import math
from typing import Any
import unittest

from chplot.plot import ZerosList, _compute_zeros, _generate_graphs, _generate_inputs
from chplot.plot import _get_unrecognized_characters
from chplot.plot import _get_x_lim, _get_x_lim_graph, _get_y_lim_graph


class MockParameters:
    def __init__(self, **attributes: dict[str, Any]) -> None:
        for field_name, field_value in attributes.items():
            setattr(self, field_name, field_value)


class TestXLim(unittest.TestCase):

    def test_correct_order(self):
        parameters = MockParameters(x_lim=(0, 1))
        self.assertTupleEqual(_get_x_lim(parameters), (0, 1))

    def test_wrong_order(self):
        parameters = MockParameters(x_lim=(1, 0))
        self.assertTupleEqual(_get_x_lim(parameters), (0, 1))


class TestXLimGraph(unittest.TestCase):

    def test_correct_order_no_log(self):
        parameters = MockParameters(x_lim=(0, 1), is_x_log=False)
        self.assertTupleEqual(_get_x_lim_graph(parameters), (0, 1))

    def test_wrong_order_no_log(self):
        parameters = MockParameters(x_lim=(1, -1), is_x_log=False)
        self.assertTupleEqual(_get_x_lim_graph(parameters), (-1, 1))

    def test_correct_order_log_positive(self):
        parameters = MockParameters(x_lim=(1, 100), is_x_log=True)
        self.assertTupleEqual(_get_x_lim_graph(parameters), (1, 100))

    def test_wrong_order_log_positive(self):
        parameters = MockParameters(x_lim=(100, 10), is_x_log=True)
        self.assertTupleEqual(_get_x_lim_graph(parameters), (10, 100))

    def test_correct_order_log_half_positive(self):
        parameters = MockParameters(x_lim=(-1, 100), is_x_log=True)
        self.assertTupleEqual(_get_x_lim_graph(parameters), (None, 100))

    def test_correct_order_log_negative(self):
        parameters = MockParameters(x_lim=(-1, -2), is_x_log=True)
        self.assertTupleEqual(_get_x_lim_graph(parameters), ())


class TestYLimGraph(unittest.TestCase):

    def test_correct_order(self):
        parameters = MockParameters(y_lim=(0, 1), must_contain_zero=False, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (0, 1))

    def test_wrong_order(self):
        parameters = MockParameters(y_lim=(1, 0), must_contain_zero=False, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (0, 1))

    # First 8 cases, y_max > 0
    # Variable : y_min > 0 or y_min <= 0 ; must contain zero or not ; log or not
    def test_positive_no_zero_no_log(self):
        parameters = MockParameters(y_lim=(1, 2), must_contain_zero=False, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (1, 2))

    def test_positive_no_zero_log(self):
        parameters = MockParameters(y_lim=(1, 2), must_contain_zero=False, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (1, 2))

    def test_positive_zero_no_log(self):
        parameters = MockParameters(y_lim=(1, 2), must_contain_zero=True, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (0, 2))

    def test_positive_zero_log(self):
        parameters = MockParameters(y_lim=(1, 2), must_contain_zero=True, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (1, 2))

    def test_half_positive_no_zero_no_log(self):
        parameters = MockParameters(y_lim=(-1, 2), must_contain_zero=False, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (-1, 2))

    def test_half_positive_no_zero_log(self):
        parameters = MockParameters(y_lim=(-1, 2), must_contain_zero=False, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (None, 2))

    def test_half_positive_zero_no_log(self):
        parameters = MockParameters(y_lim=(-1, 2), must_contain_zero=True, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (-1, 2))

    def test_half_positive_zero_log(self):
        parameters = MockParameters(y_lim=(-1, 2), must_contain_zero=True, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (None, 2))

    # Last 4 cases, y_max <= 0
    # Variable must contain zero or not ; log or not
    def test_negative_no_zero_no_log(self):
        parameters = MockParameters(y_lim=(-2, -1), must_contain_zero=False, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (-2, -1))

    def test_negative_no_zero_log(self):
        parameters = MockParameters(y_lim=(-2, -1), must_contain_zero=False, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), ())

    def test_negative_zero_no_log(self):
        parameters = MockParameters(y_lim=(-2, -1), must_contain_zero=True, is_y_log=False)
        self.assertTupleEqual(_get_y_lim_graph(parameters), (-2, 0))

    def test_negative_zero_log(self):
        parameters = MockParameters(y_lim=(-2, -1), must_contain_zero=True, is_y_log=True)
        self.assertTupleEqual(_get_y_lim_graph(parameters), ())


class TestUnrecognizedCharacters(unittest.TestCase):

    def test_no_unrecognized_characters(self):
        self.assertSetEqual(_get_unrecognized_characters('1+1', '1 1 +'), set())

    def test_normal_unrecognized_characters(self):
        self.assertSetEqual(_get_unrecognized_characters('max(1, 2)', '1 2 max'), set())
        self.assertSetEqual(_get_unrecognized_characters('max(1; 2)', '1 2 max'), set())

    def test_one_unrecognized_characters(self):
        self.assertSetEqual(_get_unrecognized_characters('x!', 'x'), {'!'})

    def test_multiple_unrecognized_characters(self):
        self.assertSetEqual(_get_unrecognized_characters('x?4$5%', 'x 4 5'), {'?', '$', '%'})


class TestComputeZeros(unittest.TestCase):

    # A list of zeros contains float 2-tuples either of the form (lower, upper) if the function is zero on an interval
    # or (x_zero, None) if the function is zero only at one point
    def assertZerosListAlmostEqual(self, computed_zeros: ZerosList, real_zeros: ZerosList):
        for (computed_lower, computed_upper), (real_lower, real_upper) in zip(computed_zeros, real_zeros):
            self.assertAlmostEqual(computed_lower, real_lower)
            self.assertAlmostEqual(computed_upper, real_upper)

    def test_no_zeros(self):
        parameters = MockParameters(expressions=['x'], x_lim=(1, 2))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [])

    def test_one_simple_zero(self):
        parameters = MockParameters(expressions=['x'], x_lim=(-1, 2))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(0.0, None)])

    def test_one_simple_float_zero(self):
        parameters = MockParameters(expressions=['x^2 - 2'], x_lim=(0, 2))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(math.sqrt(2), None)])

    def test_multiple_simple_zeros(self):
        parameters = MockParameters(expressions=['(x + 2) * x * (x - 2)'], x_lim=(-3, 3))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(-2.0, None), (0.0, None), (2.0, None)])

    def test_multiple_tangent_zero(self):
        parameters = MockParameters(expressions=['x * x'], x_lim=(-1, 1))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(0.0, None)])

    def test_multiple_small_zeros(self):
        parameters = MockParameters(expressions=['x * x - 10^(-20)'], x_lim=(-1, 1))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(-1e-10, None), (1e-10, None)])

    def test_one_zero_interval(self):
        parameters = MockParameters(expressions=['1-rect(x)'], x_lim=(-2, 2))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(-0.5, 0.5)])

    def test_one_zero_interval_one_simple_zero(self):
        parameters = MockParameters(expressions=['ifn(x, x, ifn(x - 1, 0, ifn(x - 2, x - 1, 3 - x)))'], x_lim=(-1, 4))
        inputs = _generate_inputs(parameters)
        graphs = _generate_graphs(parameters, inputs)

        self.assertZerosListAlmostEqual(_compute_zeros(inputs, graphs), [(0.0, 1.0), (3.0, None)])

