import logging
import math
from operator import add, mul, neg, pos, sub, truediv

from chplot.functions.constants import CONSTANTS_FUNCTIONS
from chplot.functions.math_functions import MATH_FUNCTIONS
from chplot.functions.mpmath_functions import MPMATH_FUNCTIONS
from chplot.functions.other_functions import OTHER_FUNCTIONS
from chplot.functions.probability_functions import PROBABILITY_FUNCTIONS
from chplot.functions.scipy_functions import SCIPY_SPECIAL_FUNCTIONS
from chplot.functions.utils import FunctionDict


logger = logging.getLogger(__name__)


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
    **OTHER_FUNCTIONS, # unpack this first, so its functions may be overriden by the next ones
    **MATH_FUNCTIONS,
    **MPMATH_FUNCTIONS,
    **SCIPY_SPECIAL_FUNCTIONS,
    **PROBABILITY_FUNCTIONS,
}
