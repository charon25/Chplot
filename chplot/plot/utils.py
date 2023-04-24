from dataclasses import dataclass
from enum import Enum
import functools
import logging
from typing import Callable, Optional, Union

import numpy as np

LOGGER = logging.getLogger('CHPLOT')


class GraphType(Enum):
    BASE = 0
    DERIVATIVE = 1
    FILE = 2
    REGRESSION = 3


@dataclass
class Graph:
    inputs: np.ndarray
    type: GraphType
    expression: str
    rpn: Optional[str]
    values: Union[list[float], np.ndarray]


ZerosList = list[tuple[float, float]]
# Characters that won't appear in the RPN but are recognized
NORMAL_UNRECOGNIZED_CHARACTERS = '( ),;e'


def plottable(arg_count: int = 1) -> Callable:
    """ Decorator allowing the function to be used with the command line interface of the chplot module.
    The function should accept a predetermined number of float and return one float (which can be nan or inf).

    Args:
        arg_count (int, optional): Number of (float) arguments expected by the function. Can be zero for constants. Defaults to 1.
    """


    def decorator_plottable(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return decorator_plottable

DECORATOR_GETTER_REGEX = r'@plottable(?:\((?:arg_count=)?(\d+)\))?'
FUNCTION_NAME_REGEX = r'def (.*?)\('


def _round(x: float, digits: int) -> float:
    """Almost equivalent to the built-in round function, but will replace -0.0 by 0.0."""

    rounded = round(x, digits)

    if rounded == 0.0:
        return 0.0
    return rounded
