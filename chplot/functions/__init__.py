import logging
import math
from operator import add, mul, sub, truediv

from chplot.functions.utils import FunctionDict
from chplot.functions.math_functions import MATH_MODULE_FUNCTION_DICT
from chplot.functions.scipy_functions import SCIPY_SPECIAL_MODULE_FUNCTION_DICT


logger = logging.getLogger('chplot')


FUNCTIONS: FunctionDict = {
    # Base operations
    '+': (2, add),
    '-': (2, sub),
    '*': (2, mul),
    '/': (2, truediv),
    '^': (2, pow),
    # Constants
    'pi': (0, math.pi),
    'tau': (0, 2 * math.pi),
    'e': (0, math.e),
    'gamma': (0, 0.5772156649015329),
    'phi': (0, 1.618033988749895),
    'sqrt2': (0, math.sqrt(2)),
    #
    **MATH_MODULE_FUNCTION_DICT,
    #
    **SCIPY_SPECIAL_MODULE_FUNCTION_DICT,

}
