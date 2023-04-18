import logging
logging.disable(logging.CRITICAL)
import unittest

from chplot.plot.plot import _get_unrecognized_characters


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
