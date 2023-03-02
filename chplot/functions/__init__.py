import logging
import math
from operator import add, mul, neg, pos, sub, truediv

from chplot.functions.constants import CONSTANTS_FUNCTIONS
from chplot.functions.math_functions import MATH_FUNCTIONS
from chplot.functions.other_functions import OTHER_FUNCTIONS
from chplot.functions.scipy_functions import SCIPY_SPECIAL_FUNCTIONS
from chplot.functions.utils import FunctionDict


logger = logging.getLogger('chplot')


FUNCTIONS: FunctionDict = {
    # Base operations
    '+': (2, add),
    '+u': (1, pos),
    '-': (2, sub),
    '-u': (1, neg),
    '*': (2, mul),
    '/': (2, truediv),
    '^': (2, pow),
    # Constants
    **CONSTANTS_FUNCTIONS,
    #
    **MATH_FUNCTIONS,
    **SCIPY_SPECIAL_FUNCTIONS,
    **OTHER_FUNCTIONS

}
