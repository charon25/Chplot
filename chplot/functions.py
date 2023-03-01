import math
from operator import add, mul, sub, truediv
from typing import Callable, Union


FunctionDict = dict[str, tuple[int, Union[Callable[..., float], float]]]

FUNCTIONS: FunctionDict = {
    # Base operations
    '+': (2, add),
    '-': (2, sub),
    '*': (2, mul),
    '/': (2, truediv),
    '^': (2, pow),
    # Constants
    'pi': (0, math.pi),
    'e': (0, math.exp(1)),
    
}