import math

from chplot.functions.utils import FunctionDict, get_functions_from_module, get_renamed_functions_from_module


_MATH_MODULE_FUNCTION_NAMES: tuple[int, str] = [
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

_MATH_MODULE_FUNCTION_RENAMED: tuple[str, int, str] = {
    ('lngamma', 1, 'lgamma'),
    ('ln', 1, 'log')
}


def _dist(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.dist((x1, y1), (x2, y2))


MATH_FUNCTIONS: FunctionDict = get_functions_from_module(math, _MATH_MODULE_FUNCTION_NAMES)

MATH_FUNCTIONS.update({
    'dist': (4, _dist),
})

MATH_FUNCTIONS.update(get_renamed_functions_from_module(math, _MATH_MODULE_FUNCTION_RENAMED))
