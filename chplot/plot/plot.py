import logging

logger = logging.getLogger(__name__)

import numpy as np
np.seterr('raise')
import matplotlib.pyplot as plt
from shunting_yard import MismatchedBracketsError, shunting_yard

from chplot.rpn import compute_rpn_list, get_rpn_errors
from chplot.plot.utils import GraphList, NORMAL_UNRECOGNIZED_CHARACTERS
from chplot.plot.plot_parameters import PlotParameters, set_default_values
from chplot.plot.zeros import compute_and_print_zeros



def _get_x_lim(parameters: PlotParameters) -> tuple[float, float]:
    """Return the minimum and maximum value for the input array. If max < min, reverse them."""
    x_min, x_max = parameters.x_lim
    if x_max < x_min:
        logger.warning('the upper x bound (%s) is inferior to the lower x bound (%s), they will be swapped.', x_max, x_min)
        return (x_max, x_min)

    return (x_min, x_max)



def _get_x_lim_graph(parameters: PlotParameters) -> tuple[float, float]:
    """Return the bounds for the plot x-axis. Will reverse if in the wrong order, and remove some negative bounds for log-scaled x-axis."""
    x_min, x_max = parameters.x_lim
    if x_max < x_min:
        x_min, x_max = x_max, x_min

    if not parameters.is_x_log:
        return (x_min, x_max)

    # If the x-axis is on a log-scale and x_min < 0, we let matplotlib decide the smallest meaningful value
    if x_min <= 0 < x_max:
        logger.warning('x-axis scale is logarithmic, but lower x bound (%s) is negative: x-axis will be truncated to positive values', x_min)
        return (None, x_max)

    if x_max <= 0:
        logger.error('x-axis scale is logarithmic, but both lower (%s) and upper (%s) x bounds are negative: cannot graph anything', x_min, x_max)
        return ()

    # Both bounds are already > 0
    return (x_min, x_max)



def _generate_inputs(parameters: PlotParameters) -> np.ndarray:
    inputs = np.linspace(*_get_x_lim(parameters), parameters.n_points, endpoint=True)

    if not parameters.is_integer:
        return inputs

    # Some points may repeat, so we keep only the unique to avoid doing useless work
    return np.unique(np.round(inputs))


def _get_unrecognized_characters(expression: str, rpn: str) -> set[str]:
    return set(expression).difference(rpn).difference(NORMAL_UNRECOGNIZED_CHARACTERS)


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

        if (unknown_characters := _get_unrecognized_characters(expression, rpn)):
            logger.warning("unknown characters in expression '%s': %s", expression, ''.join(unknown_characters))

        y = compute_rpn_list(rpn, inputs, variable=parameters.variable)
        graphs.append((expression, rpn, y))

    return graphs


def _get_y_lim_graph(parameters: PlotParameters) -> tuple[float, float]:
    """Return the bounds for the plot y-axis. Will reverse if in the wrong order, and remove some negative bounds for log-scaled y-axis."""
    y_min, y_max = plt.ylim()

    if parameters.y_lim is not None:
        y_min, y_max = parameters.y_lim
        if y_max < y_min:
            logger.warning('the upper y bound (%s) is inferior to the lower y bound (%s), they will be swapped.', y_max, y_min)
            y_min, y_max = y_max, y_min

    if parameters.must_contain_zero and parameters.is_y_log:
        logger.warning("the y-axis cannot be logarithmic while containing zero ; the '-z' argument will be ignored")

    # There are 12 possible cases depending on the parameters
    # The first separation is whether y_max is > 0 or <= 0
    if y_max > 0:
        # Here, there are 3 binary variables: y_min <= 0 or not, must contain zero or not, log scale or not
        # In all cases, the upper bound does not vary, only the lower bound
        if y_min > 0 and parameters.must_contain_zero and not parameters.is_y_log:
            y_min = 0
        elif y_min <= 0 and parameters.is_y_log:
            logger.warning('y-axis scale is logarithmic, but lower y bound (%s) is negative: y-axis will be truncated to positive values', y_min)
            y_min = None

        return (y_min, y_max)

    # If y_max <= 0, there are 4 cases and only two binary variables: must contain zero or not, log scale or not
    if parameters.is_y_log:
        logger.error('y-axis scale is logarithmic, but both lower (%s) and upper (%s) y bounds are negative: cannot graph anything', y_min, y_max)
        return ()
    
    if parameters.must_contain_zero:
        return (y_min, 0)

    return (y_min, y_max)


def _plot_graphs(parameters: PlotParameters, inputs: np.ndarray, graphs: GraphList) -> None:
    format = 'o' if parameters.is_integer else '-'
    for expression, _, y in graphs:
        plt.plot(inputs, y, format, label=expression, markersize=3)

    plt.grid(True, 'both', 'both')

    if parameters.is_x_log:
        plt.xscale('log')
    if parameters.is_y_log:
        plt.yscale('log')

    plt.xlim(_get_x_lim_graph(parameters))
    plt.ylim(_get_y_lim_graph(parameters))

    plt.xlabel(parameters.x_label)
    plt.ylabel(parameters.y_label)
    plt.title(parameters.title)

    if not parameters.remove_legend:
        plt.legend(loc=0)



def plot(parameters: PlotParameters) -> None:
    """_summary_

    Args:
        parameters (PlotParameters): Object containing all the plot parameters.
        The only mandatory attribute is 'expressions' (a list of strings).
        For all other attributes, if they are missing or set to None, the default value will be used.
        Refer to the PlotParameters class for more details.
    """

    set_default_values(parameters)

    inputs = _generate_inputs(parameters)
    graphs = _generate_graphs(parameters, inputs)

    if not graphs:
        logger.error('no expression without errors, cannot plot anything.')
        return

    if parameters.compute_zeros:
        compute_and_print_zeros(graphs)

    _plot_graphs(parameters, inputs, graphs)
    #TODO faire qqch si aucun graphe
    plt.show()
