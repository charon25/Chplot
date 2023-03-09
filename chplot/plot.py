from dataclasses import dataclass, fields
import logging
logger = logging.getLogger(__name__)
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
    is_x_log: Optional[bool]
    y_lim: Optional[tuple[float, float]]
    must_contains_zero: Optional[bool]
    is_y_log: Optional[bool]
    n_points: Optional[int]
    is_integer: Optional[bool]


DEFAULT_PARAMETERS = PlotParameters(
    expressions=[],
    variable='x',
    x_lim=(0.0, 1.0),
    is_x_log=False,
    y_lim=None,
    must_contains_zero=False,
    is_y_log=False,
    n_points=10000,
    is_integer=False,
)



def _set_default_values(parameters: PlotParameters) -> None:
    for field in fields(PlotParameters):
        fieldname = field.name
        if not hasattr(parameters, fieldname) or getattr(parameters, fieldname) is None:
            setattr(parameters, fieldname, getattr(DEFAULT_PARAMETERS, fieldname))



def _get_x_lims(parameters: PlotParameters) -> tuple[float, float]:
    x_min, x_max = parameters.x_lim
    if x_max < x_min:
        logger.warning('the upper x bound (%s) is inferior to the lower x bound (%s), they will be swapped.', x_max, x_min)
        return (x_max, x_min)

    return (x_min, x_max)



def _get_x_lims_graph(parameters: PlotParameters) -> tuple[float, float]:
    x_min, x_max = parameters.x_lim
    if x_max < x_min:
        x_min, x_max = x_max, x_min

    if not parameters.is_x_log:
        return (x_min, x_max)

    # If the x-axis is on a log-scale and x_min < 0, we force it to be smallest meaningful positive number:
    # the min of 1 and the smallest positive input
    if x_min <= 0 < x_max:
        logger.warning('x-axis scale is logarithmic, but lower x bound (%s) is negative: x-axis will be truncated to positive values', x_min)
        return (min(1, x_max / parameters.n_points), x_max)

    if x_max <= 0:
        logger.error('x-axis scale is logarithmic, but both lower (%s) and upper (%s) x bounds are negative: cannot graph anything', x_min, x_max)

    # Both bounds are already > 0
    return (x_min, x_max)



def _generate_inputs(parameters: PlotParameters) -> np.ndarray:
    inputs = np.linspace(*_get_x_lims(parameters), parameters.n_points, endpoint=True)

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



def _get_y_lims(parameters: PlotParameters) -> tuple[float, float]:
    y_min, y_max = plt.ylim()

    if parameters.y_lim is not None:
        y_min, y_max = parameters.y_lim
        if y_max < y_min:
            logger.warning('the upper y bound (%s) is inferior to the lower y bound (%s), they will be swapped.', y_max, y_min)
            y_min, y_max = y_max, y_min

    # If we do not require the y-axis to contain 0 or if it is already contained
    if not parameters.must_contains_zero or y_min <= 0 <= y_max:
        return (y_min, y_max)

    # Both are > 0, so we force y_min to 0
    if y_min > 0:
        return (0, y_max)
    # Both are < 0, so we force y_max to 0
    return (y_min, 0)



def _plot_graphs(parameters: PlotParameters, inputs: np.ndarray, graphs: GraphList) -> None:
    format = 'o' if parameters.is_integer else '-'
    for expression, y in graphs:
        plt.plot(inputs, y, format, label=expression, markersize=3)

    plt.grid(True, 'both', 'both')

    if parameters.is_x_log:
        plt.xscale('log')
    if parameters.is_y_log:
        plt.yscale('log')

    plt.xlim(_get_x_lims_graph(parameters))
    plt.ylim(_get_y_lims(parameters))

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
