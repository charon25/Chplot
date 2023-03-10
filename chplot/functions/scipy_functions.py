import logging

import scipy.special

from chplot.functions.utils import FunctionDict, get_functions_from_module


logger = logging.getLogger(__name__)


_SCIPY_SPECIAL_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    (1, 'erfcinv'),
    (3, 'betaincinv'),
    (1, 'psi'), (1, 'digamma')
]

SCIPY_SPECIAL_FUNCTIONS: FunctionDict = get_functions_from_module(scipy.special, _SCIPY_SPECIAL_MODULE_FUNCTION_NAMES)
