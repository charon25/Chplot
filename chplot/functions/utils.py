import logging
from types import ModuleType
from typing import Callable, Union


logger = logging.getLogger('chplot')

FunctionDict = dict[str, tuple[int, Union[Callable[..., float], float]]]

def get_functions_from_module(module: ModuleType, function_names: tuple[int, str]):
    # Use a for loop so we can try-except on each function separately
    # The goal is to be as resilient as possible, and add every defined function
    function_dictionary: FunctionDict = {}
    for parameter_count, function_name  in function_names:
        try:
            function_dictionary[function_name] = (parameter_count, getattr(module, function_name))
        except AttributeError:
            logger.warning("'%s' module does not contain function '%s'", module.__name__, function_name)
        except Exception:
            logger.warning("Unknown error while trying to get function '%s' of module '%s'", function_name, module.__name__)

    return function_dictionary

def get_renamed_functions_from_module(module: ModuleType, function_names: tuple[str, int, str]):
    # Use a for loop so we can try-except on each function separately
    # The goal is to be as resilient as possible, and add every defined function
    function_dictionary: FunctionDict = {}
    for new_name, parameter_count, function_name  in function_names:
        try:
            function_dictionary[new_name] = (parameter_count, getattr(module, function_name))
        except AttributeError:
            logger.warning("'%s' module does not contain function '%s'", module.__name__, function_name)
        except Exception:
            logger.warning("Unknown error while trying to get function '%s' of module '%s'", function_name, module.__name__)

    return function_dictionary
