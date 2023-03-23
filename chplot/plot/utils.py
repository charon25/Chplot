from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import numpy as np


class GraphType(Enum):
    BASE = 0
    DERIVATIVE = 1
    FILE = 2


@dataclass
class Graph:
    inputs: np.ndarray
    type: GraphType
    expression: str
    rpn: Optional[str]
    values: Union[list[float], np.ndarray]


ZerosList = list[tuple[float, float]]
# Characters that won't appear in the RPN but are recognized
NORMAL_UNRECOGNIZED_CHARACTERS = '( ),;'
