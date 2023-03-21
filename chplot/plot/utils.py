from dataclasses import dataclass
from typing import Optional, Union

import numpy as np


@dataclass
class Graph:
    inputs: np.ndarray
    expression: str
    rpn: Optional[str]
    values: Union[list[float], np.ndarray]


ZerosList = list[tuple[float, float]]
# Characters that won't appear in the RPN but are recognized
NORMAL_UNRECOGNIZED_CHARACTERS = '( ),;'
