import logging

from chplot.functions.utils import FunctionDict, get_functions_from_module, get_renamed_functions_from_module


logger = logging.getLogger(__name__)


_SCIPY_SPECIAL_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    (1, 'zeta'),
    (1, 'erfinv'), (1, 'erfcinv'),
    (2, 'beta'), (3, 'betainc'), (3, 'betaincinv'),
    (1, 'psi'), (1, 'digamma')
]
_SCIPY_SPECIAL_MODULE_FUNCTION_RENAMED: tuple[str, int, str] = {
    ('W', 1, 'lambertw'),
}

try:
    import scipy.special
    SCIPY_SPECIAL_FUNCTIONS: FunctionDict = get_functions_from_module(scipy.special, _SCIPY_SPECIAL_MODULE_FUNCTION_NAMES)
    SCIPY_SPECIAL_FUNCTIONS.update(get_renamed_functions_from_module(scipy.special, _SCIPY_SPECIAL_MODULE_FUNCTION_RENAMED))
except (ModuleNotFoundError, ImportError):
    logger.info('scipy.special is not installed, will continue without its functions.')
    SCIPY_SPECIAL_FUNCTIONS: FunctionDict = {}
