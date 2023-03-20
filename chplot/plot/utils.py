from typing import Union

import numpy as np


Graph = tuple[str, str, Union[list[float], np.ndarray]]
GraphList = list[Graph]
ZerosList = list[tuple[float, float]]
# Characters that won't appear in the RPN but are recognized
NORMAL_UNRECOGNIZED_CHARACTERS = '( ),;'
