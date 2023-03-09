import logging
from typing import Protocol

import numpy as np
import matplotlib.pyplot as plt
from shunting_yard import MismatchedBracketsError, shunting_yard

from chplot.rpn import compute_rpn_list, get_rpn_errors


logger = logging.getLogger('chplot')


class PlotParameters(Protocol):
    expressions: list[str]
    variable: str

    x_lim: tuple[float, float]
    n_points: int



def plot(parameters: PlotParameters) -> None:
    x = np.linspace(parameters.x_lim[0], parameters.x_lim[1], parameters.n_points, endpoint=True)

    graphs: list[list[float]] = []

    for expression in parameters.expressions:

        try:
            rpn = shunting_yard(expression, variable=parameters.variable)
        except MismatchedBracketsError:
            logger.error("mismatched brackets in the expression '%s'", expression)
            continue

        if (error := get_rpn_errors(rpn)) is not None:
            logger.error("error for expression '%s' : %s", expression, error)
            continue

        y = compute_rpn_list(rpn, x)
        graphs.append(y)
    
    plt.plot(x, y)
    plt.show()
