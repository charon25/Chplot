import math
import unittest

from chplot.rpn import compute_rpn_list, compute_rpn_unsafe

class TestRpnList(unittest.TestCase):

    def test_rpn_simple(self):
        rpn = "1 x +"
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [2, 3, 4, 5])

    def test_rpn_multiple_variable(self):
        rpn = "x x * x +"
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [2, 6, 12, 20])

    def test_rpn_change_variable(self):
        rpn = "y y *"
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs, variable='y')), [1, 4, 9, 16])

    def test_rpn_change_long_list(self):
        rpn = "x x *"
        inputs = range(10000)

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), list(x * x for x in range(10000)))

    def test_rpn_change_invalid_operation(self):
        rpn = "1 x / 10 *"
        inputs = [-2, -1, 0, 1, 2]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [-5.0, -10.0, math.nan, 10.0, 5.0])

    def test_constants(self):
        rpn = "pi x +"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1 + math.pi)

