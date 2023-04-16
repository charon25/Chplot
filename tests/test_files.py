import logging

import numpy as np
logging.disable(logging.CRITICAL)
import re
import unittest

from tests.mock_parameters import MockParameters
from chplot.plot.files import DecimalSeparator, IllegalQuotesError, REGEX_ILLEGAL_QUOTES
from chplot.plot.files import _get_column_names, _get_line_format, _read_files
from chplot.plot.utils import Graph, GraphType


def fp(filename):
    return f'tests\\test_files\\data_files\\{filename}.csv'

class TestGetLineFormat(unittest.TestCase):

    def test_empty_array(self):
        self.assertTupleEqual(_get_line_format([]), ('', DecimalSeparator.UNKNOWN))
        self.assertTupleEqual(_get_line_format(['', '']), ('', DecimalSeparator.UNKNOWN))
        self.assertTupleEqual(_get_line_format(['', '', 'x,y,z']), ('', DecimalSeparator.UNKNOWN))

    def test_one_line(self):
        self.assertTupleEqual(_get_line_format(['1,2,3']), (',', DecimalSeparator.DOT))
        self.assertTupleEqual(_get_line_format(['1;2;3']), (';', DecimalSeparator.UNKNOWN))
        self.assertTupleEqual(_get_line_format(['1\t2\t3']), ('\t', DecimalSeparator.UNKNOWN))
        self.assertTupleEqual(_get_line_format(['1 2 3']), (' ', DecimalSeparator.UNKNOWN))

    def test_with_empty_lines(self):
        self.assertTupleEqual(_get_line_format(['', '', '1,2,3', '']), (',', DecimalSeparator.DOT))

    def test_float_values(self):
        self.assertTupleEqual(_get_line_format(['1.2,2.3,3.4']), (',', DecimalSeparator.DOT))
        self.assertTupleEqual(_get_line_format(['1,2;2,3;3,4']), (';', DecimalSeparator.COMMA))

    def test_with_title(self):
        self.assertTupleEqual(_get_line_format(['x,y,z', '', '1,2,3', '']), (',', DecimalSeparator.DOT))
        self.assertTupleEqual(_get_line_format(['x,y,z', '', '1;2;3', '']), (';', DecimalSeparator.UNKNOWN))


class TestRegexIllegalQuotes(unittest.TestCase):

    def test_no_quotes_at_all(self):
        self.assertNotRegex('', REGEX_ILLEGAL_QUOTES)
        self.assertNotRegex('text', REGEX_ILLEGAL_QUOTES)

    def test_only_legal_quotes(self):
        # Any number of quotes at the beginning and or at the end
        # + any even number of quotes in the middle
        for n in range(10):
            for m in range(10):
                for k in range(2, 10, 2):
                    text = ''.join(('"' * n, 'te', '"' * k, 'xt', '"' * m))
                    self.assertNotRegex(text, REGEX_ILLEGAL_QUOTES)

    def test_only_illegal_quotes(self):
        # Any odd number of quotes stricly inside the string
        for k in range(1, 10, 2):
            text = ''.join(('te', '"' * k, 'xt',))
            self.assertRegex(text, REGEX_ILLEGAL_QUOTES)

    def test_both(self):
        # Any number of quotes at the beginning and or at the end
        # + any even number of quotes in the middle
        # + any odd number of quotes in the middle
        for n in range(10):
            for m in range(10):
                for k in range(2, 10, 2): # even
                    for j in range(1, 10, 2): # odd
                        text = ''.join(('"' * n, 'st', '"' * k, 'ri', '"' * j, 'ng', '"' * m))
                        self.assertRegex(text, REGEX_ILLEGAL_QUOTES)


class TestGetColumnNames(unittest.TestCase):

    def test_basic(self):
        self.assertListEqual(_get_column_names('abc,def,ghi', ','), ['abc', 'def', 'ghi'])
        self.assertListEqual(_get_column_names('abc;def;ghi', ';'), ['abc', 'def', 'ghi'])
        self.assertListEqual(_get_column_names('abc\tdef\tghi', '\t'), ['abc', 'def', 'ghi'])
        self.assertListEqual(_get_column_names('abc def ghi', ' '), ['abc', 'def', 'ghi'])

    def test_quotes(self):
        self.assertListEqual(_get_column_names('abc,"def",ghi', ','), ['abc', 'def', 'ghi'])
        self.assertListEqual(_get_column_names('abc,"d,ef",ghi', ','), ['abc', 'd,ef', 'ghi'])
        self.assertListEqual(_get_column_names('abc,"d,e,f",ghi', ','), ['abc', 'd,e,f', 'ghi'])

    def test_double_quotes(self):
        self.assertListEqual(_get_column_names('abc,d""ef,ghi', ','), ['abc', 'd"ef', 'ghi'])
        self.assertListEqual(_get_column_names('abc,"d""ef",ghi', ','), ['abc', 'd"ef', 'ghi'])
        self.assertListEqual(_get_column_names('abc,"d"",e""f",ghi', ','), ['abc', 'd",e"f', 'ghi'])

    def test_illegal_quotes(self):
        with self.assertRaises(IllegalQuotesError):
            _get_column_names('abc,"de"f,ghi', ',')
        with self.assertRaises(IllegalQuotesError):
            _get_column_names('abc,d"ef",ghi', ',')
        with self.assertRaises(IllegalQuotesError):
            _get_column_names('abc,d"ef,ghi', ',')


class TestReadFile(unittest.TestCase):

    def assertGraphEqual(self, graph: Graph, inputs: list[float], expression: str, values: list[float]):
        self.assertEqual(graph.type, GraphType.FILE)
        self.assertTrue(np.array_equal(graph.inputs, inputs))
        self.assertEqual(graph.expression, expression)
        self.assertListEqual(graph.values, values)


    def test_empty_file(self):
        parameters = MockParameters(data_files=[fp("empty")])
        self.assertListEqual(_read_files(parameters), [])

    def test_comma_integers(self):
        parameters = MockParameters(data_files=[fp("comma_integers")])
        graphs = _read_files(parameters)
        self.assertGraphEqual(graphs[0], [0, 1, 2], 'comma_integers.csv - colB', [3, 4, 5])
        self.assertGraphEqual(graphs[1], [0, 1, 2], 'comma_integers.csv - colC', [6, 7, 8])

    def test_all_format(self):
        files = ('comma_dot', 'semicolon_dot', 'space_dot', 'tab_dot', 'semicolon_comma')
        for file in files:
            parameters = MockParameters(data_files=[fp(file)])
            graphs = _read_files(parameters)
            self.assertGraphEqual(graphs[0], [0.5, 1.5, 2.5], f'{file}.csv - colB', [3.5, 4.5, 5.5])
            self.assertGraphEqual(graphs[1], [0.5, 1.5, 2.5], f'{file}.csv - colC', [6.5, 7.5, 8.5])

    def test_irregular_column_sizes(self):
        parameters = MockParameters(data_files=[fp("irregular_columns_size")])
        graphs = _read_files(parameters)
        self.assertGraphEqual(graphs[0], [0, 1, 2, 12], 'irregular_columns_size.csv - colB', [3, 4, 5, 13])
        self.assertGraphEqual(graphs[1], [0, 1, 2], 'irregular_columns_size.csv - colC', [6, 7, 8])
        self.assertGraphEqual(graphs[2], [1, 2], 'irregular_columns_size.csv - colD', [9, 10])
        self.assertGraphEqual(graphs[3], [0, 1], 'irregular_columns_size.csv - colE', [14, 11])

    def test_complicated_column_names(self):
        parameters = MockParameters(data_files=[fp("complicated_column_names")])
        graphs = _read_files(parameters)
        self.assertGraphEqual(graphs[0], [0, 1, 2], 'complicated_column_names.csv - colC x', [3, 4, 5])
        self.assertGraphEqual(graphs[1], [0, 1, 2], 'complicated_column_names.csv - colD;"E', [6, 7, 8])
        self.assertGraphEqual(graphs[2], [0, 1, 2], 'complicated_column_names.csv - colF",colG', [9, 10, 11])

    def test_not_enough_column_names(self):
        parameters = MockParameters(data_files=[fp("not_enough_column_names")])
        graphs = _read_files(parameters)
        self.assertGraphEqual(graphs[0], [0, 1, 2], 'not_enough_column_names.csv - Column 1', [3, 4, 5])
        self.assertGraphEqual(graphs[1], [0, 1, 2], 'not_enough_column_names.csv - Column 2', [6, 7, 8])

    def test_no_column_names(self):
        parameters = MockParameters(data_files=[fp("no_column_names")])
        graphs = _read_files(parameters)
        self.assertGraphEqual(graphs[0], [0, 1, 2], 'no_column_names.csv - Column 1', [3, 4, 5])
        self.assertGraphEqual(graphs[1], [0, 1, 2], 'no_column_names.csv - Column 2', [6, 7, 8])

