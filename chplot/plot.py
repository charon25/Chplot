from dataclasses import dataclass, fields
import logging
logger = logging.getLogger('chplot')
from typing import Optional

import numpy as np
np.seterr('raise')
import matplotlib.pyplot as plt
from shunting_yard import MismatchedBracketsError, shunting_yard

from chplot.rpn import compute_rpn_list, get_rpn_errors


GraphList = list[tuple[str, list[float]]]

@dataclass
class PlotParameters:
    expressions: list[str]
    variable: Optional[str]

    x_lim: Optional[tuple[float, float]]
    n_points: Optional[int]
    is_integer: Optional[bool]


DEFAULT_PARAMETERS = PlotParameters(
    expressions=[],
    variable='x',
    x_lim=(0.0, 1.0),
    n_points=10000,
    is_integer=False,
)


def _set_default_values(parameters: PlotParameters) -> None:
    for field in fields(PlotParameters):
        fieldname = field.name
        if not hasattr(parameters, fieldname) or getattr(parameters, fieldname) is None:
            setattr(parameters, fieldname, getattr(DEFAULT_PARAMETERS, fieldname))


def _generate_inputs(parameters: PlotParameters) -> np.ndarray:
    inputs = np.linspace(parameters.x_lim[0], parameters.x_lim[1], parameters.n_points, endpoint=True)

    if not parameters.is_integer:
        return inputs

    # Some points may repeat, so we keep only the unique to avoid doing useless work
    return np.unique(np.round(inputs))


def _generate_graphs(parameters: PlotParameters, inputs: np.ndarray) -> GraphList:
    graphs: GraphList = []

    for expression in parameters.expressions:
        try:
            rpn = shunting_yard(expression, case_sensitive=True, variable=parameters.variable)
        except MismatchedBracketsError:
            logger.error("mismatched brackets in the expression '%s'", expression)
            continue

        if (error := get_rpn_errors(rpn, variable=parameters.variable)) is not None:
            logger.error("error for expression '%s' : %s", expression, error)
            continue

        y = compute_rpn_list(rpn, inputs, variable=parameters.variable)
        graphs.append((expression, y))
    
    return graphs


def _plot_graphs(parameters: PlotParameters, inputs: np.ndarray, graphs: GraphList) -> None:
    format = 'o' if parameters.is_integer else '-'
    for expression, y in graphs:
        plt.plot(inputs, y, format, label=expression, markersize=3)

    plt.grid(True, 'both', 'both')
    plt.legend(loc=0)



def plot(parameters: PlotParameters) -> None:
    """_summary_

    Args:
        parameters (PlotParameters): Object containing all the plot parameters.
        The only mandatory attribute is 'expressions' (a list of strings).
        For all other attributes, if they are missing or set to None, the default value will be used.
        Refer to the PlotParameters class for more details.
    """

    _set_default_values(parameters)

    inputs = _generate_inputs(parameters)
    graphs = _generate_graphs(parameters, inputs)
  
    _plot_graphs(parameters, inputs, graphs)
    #TODO faire qqch si aucun graphe
    plt.show()
