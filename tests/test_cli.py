import logging
logging.disable(logging.CRITICAL)
import unittest

from chplot.convert_args import retrieve_constants
from mock_parameters import MockParameters


class TestRetrieveConstants(unittest.TestCase):
    """The tests should be run (python -m unittest discover tests) from the parent directory in order for the filepath to be correct."""

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
        parameters = MockParameters(constants_arg=["tests\\test_files\\constants_empty.txt"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, [])

    def test_one_file_no_value(self):
        parameters = MockParameters(constants_arg=["tests\\test_files\\constants_1.txt"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["a=1"])

    def test_two_files_no_value(self):
        parameters = MockParameters(constants_arg=["tests\\test_files\\constants_1.txt", "tests\\test_files\\constants_3.txt"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["a=1", "b=2", "c=3", "d=4"])

    def test_two_files_three_values(self):
        parameters = MockParameters(constants_arg=["x=1", "tests\\test_files\\constants_1.txt", "y=2", "tests\\test_files\\constants_3.txt", "z=3"])
        retrieve_constants(parameters)
        self.assertListEqual(parameters.constants, ["x=1", "a=1", "y=2", "b=2", "c=3", "d=4", "z=3"])


