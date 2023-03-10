import logging
logging.disable(logging.CRITICAL)
from typing import Any
import unittest

from chplot.plot import _get_x_lim, _get_x_lim_graph, _get_y_lim_graph, PlotParameters


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




