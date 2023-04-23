import math
import unittest
from chplot.functions import load_necessary_functions

from chplot.rpn import compute_rpn_list, compute_rpn_unsafe, get_rpn_errors, pre_compute_rpn


class TestRpnValidity(unittest.TestCase):

    def test_no_problems(self):
        rpn = '1 1 +'
        self.assertIsNone(get_rpn_errors(rpn))

    def test_unknown_function(self):
        rpn = '1 unknown_func'
        error_message = "unknown function: 'unknown_func'"
        self.assertEqual(get_rpn_errors(rpn), error_message)

    def test_not_enough_parameters(self):
        rpn = '1 +'
        error_message = "not enough parameters for function '+': 1 found, 2 expected."
        self.assertEqual(get_rpn_errors(rpn), error_message)

    def test_too_many_results(self):
        rpn = '1 1'
        error_message = 'expression does not give only one result.'
        self.assertEqual(get_rpn_errors(rpn), error_message)


class TestRpnUnsafe(unittest.TestCase):

    def test_constants(self):
        rpn = 'pi x +'
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1 + math.pi)

    def test_math_functions(self):
        rpn = '2 sqrt'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), math.sqrt(2))

    def test_scipy_functions(self):
        rpn = '2 zeta'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1.6449340668482264)

    def test_mpmath_functions(self):
        rpn = '0 sec'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 1.0)

    def test_probability_functions(self):
        rpn = '0 0 1 normcdf'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 0.5)

    def test_probability_scipy_functions(self):
        rpn = '0.5 1 3 gammacdf'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 0.7768698398515702)

    def test_other_functions(self):
        rpn = '1.2 1 2 10 20 lerp'
        load_necessary_functions([rpn])
        self.assertAlmostEqual(compute_rpn_unsafe(rpn.split(' '), 1), 12)

    def test_infinity_is_nan(self):
        rpn = 'x zeta'
        load_necessary_functions([rpn])
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), 1)))

    def test_error_is_nan(self):
        rpn = 'x sqrt'
        load_necessary_functions([rpn])
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), -1)))

    def test_nan_constant(self):
        rpn = 'nan'
        load_necessary_functions([rpn])
        self.assertTrue(math.isnan(compute_rpn_unsafe(rpn.split(' '), 0)))


class TestPreComputeRPN(unittest.TestCase):

    def test_one_token(self):
        rpn = 'x'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), rpn.split(' '))
        rpn = '1'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), rpn.split(' '))

    def test_no_constants(self):
        rpn = 'x x +'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), rpn.split(' '))

    def test_no_constant_part(self):
        rpn = 'x 1 +'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), rpn.split(' '))

    def test_no_constant_part_with_function(self):
        rpn = 'x 1 min'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), rpn.split(' '))

    def test_one_constant_part(self):
        rpn = 'x 1 2 + *'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 3.0, '*'])

    def test_two_constant_part(self):
        rpn = 'x 1 1 + * 10 2 ^ +'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 2.0, '*', 100.0, '+'])

    def test_named_constant_in_constant_part(self):
        rpn = 'x pi *'
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 3.141592653589793, '*'])

    def test_function_in_constant_part(self):
        rpn = 'x 4 sqrt *'
        load_necessary_functions([rpn])
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 2.0, '*'])

    def test_multiple_functions_in_constant_part(self):
        rpn = 'x 2 zeta zeta zeta *'
        load_necessary_functions([rpn])
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 1.508337851767236, '*'])

    def test_functions_multiple_args_in_constant_part(self):
        rpn = 'x 5 1 2 3 min3 e max3 *'
        load_necessary_functions([rpn])
        self.assertListEqual(pre_compute_rpn(rpn.split(' ')), ['x', 5.0, '*'])


class TestRpnList(unittest.TestCase):

    def test_rpn_simple(self):
        rpn = '1 x +'
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [2, 3, 4, 5])

    def test_rpn_multiple_variable(self):
        rpn = 'x x * x +'
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [2, 6, 12, 20])

    def test_rpn_change_variable(self):
        rpn = 'y y *'
        inputs = [1, 2, 3, 4]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs, variable='y')), [1, 4, 9, 16])

    def test_rpn_change_long_list(self):
        rpn = 'x x *'
        inputs = range(10000)

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), list(x * x for x in range(10000)))

    def test_rpn_change_invalid_operation(self):
        rpn = '1 x / 10 *'
        inputs = [-2, -1, 0, 1, 2]

        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [-5.0, -10.0, math.nan, 10.0, 5.0])

    def test_rpn_inf_to_nan(self):
        rpn = 'x zeta'
        inputs = [1, 2, 3]
        load_necessary_functions([rpn])

        # The values are zeta(2) and zeta(3)
        self.assertListEqual(list(compute_rpn_list(rpn, inputs)), [math.nan, 1.6449340668482264, 1.2020569031595942])
