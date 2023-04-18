import math
import unittest

from chplot.rpn import compute_rpn_list, compute_rpn_unsafe, get_rpn_errors


class TestRpnValidity(unittest.TestCase):

    def test_no_problems(self):
        rpn = "1 1 +"
        self.assertIsNone(get_rpn_errors(rpn))

    def test_unknown_function(self):
        rpn = "1 unknown_func"
        error_message = "unknown function: 'unknown_func'"
        self.assertEqual(get_rpn_errors(rpn), error_message)

    def test_not_enough_parameters(self):
        rpn = "1 +"
        error_message = "not enough parameters for function '+': 1 found, 2 expected."
        self.assertEqual(get_rpn_errors(rpn), error_message)

    def test_too_many_results(self):
        rpn = "1 1"
        error_message = "expression does not give only one result."
        self.assertEqual(get_rpn_errors(rpn), error_message)

class TestRpnUnsafe(unittest.TestCase):

    def test_constants(self):
        rpn = "pi x +"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1 + math.pi)

    def test_math_functions(self):
        rpn = "2 sqrt"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), math.sqrt(2))

    def test_scipy_functions(self):
        rpn = "2 zeta"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1.6449340668482264)

    def test_probability_functions(self):
        rpn = "0 0 1 normcdf"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 0.5)

    def test_probability_scipy_functions(self):
        rpn = "0.5 1 3 gammacdf"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 0.7768698398515702)

    def test_other_functions(self):
        rpn = "1.2 1 2 10 20 lerp"
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 12)

    def test_infinity_is_nan(self):
        rpn = "x zeta"
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), 1)))

    def test_error_is_nan(self):
        rpn = "x sqrt"
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), -1)))

    def test_nan_constant(self):
        rpn = "nan"
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), 0)))


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

    def test_rpn_inf_to_nan(self):
        rpn = "x zeta"
        inputs = [1, 2, 3]

        # The values are zeta(2) and zeta(3)
        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [math.nan, 1.6449340668482264, 1.2020569031595942])
