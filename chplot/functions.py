import math
from operator import add, mul, sub, truediv
from typing import Callable, Union


FunctionDict = dict[str, tuple[int, Union[Callable[..., float], float]]]

MATH_MODULE_FUNCTIONS: tuple[int, str] = [
    (1, 'cos'), (1, 'sin'), (1, 'tan'),
    (1, 'acos'), (1, 'asin'), (1, 'atan'), (2, 'atan2'),
    (1, 'cosh'), (1, 'sinh'), (1, 'tanh'),
    (1, 'acosh'), (1, 'asinh'), (1, 'atanh'),
    (1, 'sqrt'), (1, 'cbrt'),
    (1, 'ceil'), (1, 'floor'),
    (1, 'degrees'), (1, 'radians'),
    (1, 'erf'), (1, 'erfc'),
    (1, 'exp'), (1, 'expm1'),
    (1, 'log'), (1, 'log10'), (1, 'log1p'), (1, 'log2'),
    (1, 'gamma'), (1, 'lgamma'),
    (2, 'fmod'), (2, 'remainder'),
    (2, 'hypot'),
    (2, 'copysign'),
    (1, 'trunc')
]

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
    # Math module
    **{name: (parameter_count, getattr(math, name)) for name, parameter_count in MATH_MODULE_FUNCTIONS},
}
