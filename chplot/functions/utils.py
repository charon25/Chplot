import logging
from types import ModuleType
from typing import Callable, Optional, Union


LOGGER = logging.getLogger('CHPLOT')

FunctionDict = dict[str, tuple[int, Union[Callable[..., float], float]]]
FunctionNames = list[tuple[str, int, Optional[str]]]

def get_functions_from_module(module: ModuleType, function_names: tuple[int, str]):
    # Use a for loop so we can try-except on each function separately
    # The goal is to be as resilient as possible, and add every defined function
    function_dictionary: FunctionDict = {}
    for parameter_count, function_name  in function_names:
        try:
            function_dictionary[function_name] = (parameter_count, getattr(module, function_name))
        except AttributeError:
            LOGGER.error("'%s' module does not contain function '%s'", module.__name__, function_name)
        except Exception:
            LOGGER.error("unknown error while trying to get function '%s' of module '%s'", function_name, module.__name__)

    return function_dictionary

def get_renamed_functions_from_module(module: ModuleType, function_names: tuple[str, int, str]):
    # Use a for loop so we can try-except on each function separately
    # The goal is to be as resilient as possible, and add every defined function
    function_dictionary: FunctionDict = {}
    for new_name, parameter_count, function_name  in function_names:
        try:
            function_dictionary[new_name] = (parameter_count, getattr(module, function_name))
        except AttributeError:
            LOGGER.error("'%s' module does not contain function '%s'", module.__name__, function_name)
        except Exception:
            LOGGER.error("unknown error while trying to get function '%s' of module '%s'", function_name, module.__name__)

    return function_dictionary

def _get_functions_from_module(module: ModuleType, function_names: FunctionNames) -> FunctionDict:
    # Use a for loop so we can try-except on each function separately
    # The goal is to be as resilient as possible, and add every defined function
    function_dictionary: FunctionDict = {}
    for new_name, parameter_count, function_name in function_names:
        try:
            if function_name is None:
                function_name = new_name
            function_dictionary[new_name] = (parameter_count, getattr(module, function_name))
        except AttributeError:
            LOGGER.error("'%s' module does not contain function '%s'", module.__name__, function_name)
        except Exception:
            LOGGER.error("unknown error while trying to get function '%s' of module '%s'", function_name, module.__name__)

    return function_dictionary


def contains_function(function_names: FunctionNames, tokens: set[str]) -> bool:
    for func_name, _, _ in function_names:
        if func_name in tokens:
            return True
    
    return False
