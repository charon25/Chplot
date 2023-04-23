from operator import add, mul, neg, pos, sub, truediv

from chplot.functions.constants import CONSTANTS_FUNCTIONS
from chplot.functions.names import MATH_FUNCTION_NAMES, MPMATH_FUNCTION_NAMES, OTHER_FUNCTION_NAMES, PROBABILITY_FUNCTION_NAMES, SCIPY_SPECIAL_FUNCTION_NAMES
from chplot.functions.utils import FunctionDict, contains_function, _get_functions_from_module



# This global variable can and will be modified to add to functions
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
    # Built-ins
    'abs': (1, abs),
    'min': (2, min), 'min3': (3, min), 'min4': (4, min),
    'max': (2, max), 'max3': (3, max), 'max4': (4, max),
}


def load_necessary_functions(rpns: list[str]) -> None:
    tokens = set()
    for rpn in rpns:
        tokens.update(rpn.split(' '))

    # Repetitive but necessary, as we do not want to import anything not needed

    if contains_function(MATH_FUNCTION_NAMES, tokens):
        import chplot.functions.definitions.math_functions as math_functions
        FUNCTIONS.update(_get_functions_from_module(math_functions, MATH_FUNCTION_NAMES))

    if contains_function(SCIPY_SPECIAL_FUNCTION_NAMES, tokens):
        import chplot.functions.definitions.scipy_special_functions as scipy_special_functions
        FUNCTIONS.update(_get_functions_from_module(scipy_special_functions, SCIPY_SPECIAL_FUNCTION_NAMES))

    if contains_function(MPMATH_FUNCTION_NAMES, tokens):
        import chplot.functions.definitions.mpmath_functions as mpmath_functions
        FUNCTIONS.update(_get_functions_from_module(mpmath_functions, MPMATH_FUNCTION_NAMES))

    if contains_function(PROBABILITY_FUNCTION_NAMES, tokens):
        import chplot.functions.definitions.probability_functions as probability_functions
        FUNCTIONS.update(_get_functions_from_module(probability_functions, PROBABILITY_FUNCTION_NAMES))

    if contains_function(OTHER_FUNCTION_NAMES, tokens):
        import chplot.functions.definitions.other_functions as other_functions
        FUNCTIONS.update(_get_functions_from_module(other_functions, OTHER_FUNCTION_NAMES))
