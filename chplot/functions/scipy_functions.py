import logging

from chplot.functions.utils import FunctionDict, get_function_dictionary


logger = logging.getLogger('chplot')

# Scipy special (only if installed)

SCIPY_SPECIAL_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    
]

try:
    import scipy.special
    SCIPY_SPECIAL_MODULE_FUNCTION_DICT: FunctionDict = get_function_dictionary(scipy.special, SCIPY_SPECIAL_MODULE_FUNCTION_NAMES)
except ModuleNotFoundError:
    logger.info('Scipy is not installed, will continue without its functions.')
    SCIPY_SPECIAL_MODULE_FUNCTION_DICT: FunctionDict = {}
