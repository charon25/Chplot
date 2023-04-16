import logging
logging.disable(logging.CRITICAL)
import re
import unittest

from chplot.plot.files import REGEX_ILLEGAL_QUOTES, IllegalQuotesError, _get_column_names, _get_line_format, DecimalSeparator


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

    ...
    # autant de chaque colonne:
    #   - , .
    #   - ; .
    #   -   .
    #   - \t .
    #   - ; ,
    # certaines lignes de données avec plus de données
    # pas assez de nom de colonnes
    # pas de nom de colonnes
