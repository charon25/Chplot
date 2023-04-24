import csv
import math
from typing import Any

import numpy as np
import matplotlib.pyplot as plt
from shunting_yard import MismatchedBracketsError, shunting_yard

from chplot.functions import FUNCTIONS, load_necessary_functions
from chplot.plot.derivative import compute_derivatives
from chplot.plot.files import read_files
from chplot.plot.integral import compute_and_print_integrals
from chplot.plot.plot_parameters import convert_parameters_expression, PlotParameters, replace_implicit_variable_multiplication, retrieve_python_functions, set_default_values
from chplot.plot.regression import compute_regressions
from chplot.plot.utils import _round as round
from chplot.plot.utils import Graph, NORMAL_UNRECOGNIZED_CHARACTERS, GraphType
from chplot.plot.utils import LOGGER
from chplot.plot.zeros import compute_and_print_zeros
from chplot.rpn import compute_rpn_list, get_rpn_errors



def _load_functions(parameters: PlotParameters) -> None:
    """Compute the RPN of every expression, and load all functions necessary to compute them."""
    all_expressions: list[str] = [
        *parameters.expressions,
        *parameters.x_lim,
        *parameters.y_lim,
        parameters.regression_expression,
    ]

    # Separate constants to check for error in the parsing
    # But do not act on the error here
    for constant in parameters.constants:
        try:
            all_expressions.append(constant.split('=')[1])
        except Exception:
            pass

    all_rpns: list[str] = []

    for expression in all_expressions:
        try:
            all_rpns.append(shunting_yard(
                expression,
                case_sensitive=True,
                variable=parameters.variable,
                convert_scientific_notation=not parameters.disable_scientific_notation,
            ))
        # The exception will be logged later when the RPN is re-computed in the relevant place
        # Here, just ignore it
        except Exception:
            pass
    
    load_necessary_functions(all_rpns)


def _get_x_lim(parameters: PlotParameters) -> tuple[float, float]:
    """Return the minimum and maximum value for the input array. If max < min, reverse them."""
    x_min, x_max = parameters.x_lim

    if x_min is None:
        x_min = 0
    if x_max is None:
        x_max = 1

    if x_max == x_min:
        LOGGER.warning('upper and lower bounds of the x-axis equal to each other (%s)', x_min)

    if x_max < x_min:
        LOGGER.warning('the upper bound (%s) of the x-axis is inferior to the lower bound (%s), they will be swapped', x_max, x_min)
        return (x_max, x_min)

    return (x_min, x_max)



def _get_x_lim_graph(parameters: PlotParameters, graphs: list[Graph]) -> tuple[float, float]:
    """Return the bounds for the plot x-axis. Will reverse if in the wrong order, and remove some negative bounds for log-scaled x-axis."""
    x_min_graph = min((graph.inputs.min() for graph in graphs), default=math.inf)
    x_max_graph = max((graph.inputs.max() for graph in graphs), default=-math.inf)

    x_min, x_max = parameters.x_lim

    # If user did not specify a min, use the min of the graphs
    if x_min is None:
        x_min = x_min_graph
    # Else, notify them if the min of the graphs is lower
    else:
        if x_min_graph < x_min:
            LOGGER.info('lower bound of the x-axis was decreased to %s to accomodate all data', round(x_min_graph, 3))
            x_min = x_min_graph

    # Same but reversed for the max
    if x_max is None:
        x_max = x_max_graph
    else:
        if x_max_graph > x_max:
            LOGGER.info('upper bound of the x-axis was increased to %s to accomodate all data', round(x_max_graph, 3))
            x_max = x_max_graph

    if x_min > x_max:
        x_min, x_max = x_max, x_min

    if not parameters.is_x_log:
        return (x_min, x_max)

    # If the x-axis is on a log-scale and x_min < 0, we let matplotlib decide the smallest meaningful value
    if x_min <= 0 < x_max:
        LOGGER.warning('x-axis scale is logarithmic, but its lower bound (%s) is negative, x-axis will be truncated to positive values', x_min)
        return (None, x_max)

    if x_max <= 0:
        LOGGER.critical('x-axis scale is logarithmic, but both its lower (%s) and upper (%s) bounds are negative, cannot graph anything', x_min, x_max)
        return (None, None)

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


def _generate_graphs(parameters: PlotParameters, inputs: np.ndarray) -> list[Graph]:
    graphs: list[Graph] = []

    if parameters.variable in FUNCTIONS:
        LOGGER.warning("variable '%s' is overriding function or constant '%s'", parameters.variable, parameters.variable)

    for expression in parameters.expressions:
        try:
            rpn = shunting_yard(
                expression=expression,
                case_sensitive=True,
                variable=parameters.variable,
                convert_scientific_notation=not parameters.disable_scientific_notation
            )
        except MismatchedBracketsError:
            LOGGER.error("mismatched brackets in the plotted expression '%s'", expression)
            continue
        except Exception:
            LOGGER.error("unknown error in the plotted expression '%s'", expression)
            continue

        if (error := get_rpn_errors(rpn, variable=parameters.variable)) is not None:
            LOGGER.error("error for expression '%s' : %s", expression, error)
            continue

        if (unknown_characters := _get_unrecognized_characters(expression, rpn)):
            LOGGER.warning("unknown characters in expression '%s': %s", expression, ''.join(unknown_characters))

        values = compute_rpn_list(rpn, inputs, variable=parameters.variable)
        graphs.append(Graph(inputs, GraphType.BASE, expression, rpn, values))

    return graphs


def _get_y_lim_graph(parameters: PlotParameters) -> tuple[float, float]:
    """Return the bounds for the plot y-axis. Will reverse if in the wrong order, and remove some negative bounds for log-scaled y-axis."""
    y_min, y_max = plt.ylim()

    # Override with non-None value given by users
    if parameters.y_lim[0] is not None:
        y_min = parameters.y_lim[0]
    if parameters.y_lim[1] is not None:
        y_max = parameters.y_lim[1]

    if y_min == y_max:
        LOGGER.warning('upper and lower bounds of the y-axis equal to each other (%s), matplotlib will automatically adjust the bounds', y_min)

    if y_max < y_min:
        LOGGER.warning('the upper bound (%s) of the y-axis is inferior to the lower bound (%s), they will be swapped', y_max, y_min)
        y_min, y_max = y_max, y_min

    if parameters.must_contain_zero and parameters.is_y_log:
        LOGGER.warning("the y-axis cannot be logarithmic while containing zero ; the '-z' argument will be ignored")

    # There are 12 possible cases depending on the parameters
    # The first separation is whether y_max is > 0 or <= 0
    if y_max > 0:
        # Here, there are 3 binary variables: y_min <= 0 or not, must contain zero or not, log scale or not
        # In all cases, the upper bound does not vary, only the lower bound
        if y_min > 0 and parameters.must_contain_zero and not parameters.is_y_log:
            y_min = 0
        elif y_min <= 0 and parameters.is_y_log:
            LOGGER.warning('y-axis scale is logarithmic, but its lower bound (%s) is negative, y-axis will be truncated to positive values', y_min)
            y_min = None

        return (y_min, y_max)

    # If y_max <= 0, there are 4 cases and only two binary variables: must contain zero or not, log scale or not
    if parameters.is_y_log:
        LOGGER.critical('y-axis scale is logarithmic, but both its lower (%s) and upper (%s) bounds are negative: cannot graph anything', y_min, y_max)
        return ()

    if parameters.must_contain_zero:
        return (y_min, 0)

    return (y_min, y_max)


def _get_graph_parameters(parameters: PlotParameters, graph: Graph) -> dict[str, Any]:
    if graph.type == GraphType.REGRESSION:
        return {'linestyle': '--', 'markersize': 0}

    if parameters.is_integer or parameters.markersize:
        return {'linestyle': ' ', 'marker': 'o', 'markersize': parameters.markersize or 3}

    return {'linestyle': '-', 'linewidth': parameters.line_width}


def _plot_graphs(parameters: PlotParameters, graphs: list[Graph]) -> None:
    if parameters.square_graph:
        plt.gca().set_aspect('equal')

    for graph in graphs:
        graph_parameters = _get_graph_parameters(parameters, graph)
        plt.plot(graph.inputs, graph.values, label=graph.expression, **graph_parameters)

    plt.grid(True, 'both', 'both')

    if parameters.is_x_log:
        plt.xscale('log')
    if parameters.is_y_log:
        plt.yscale('log')

    plt.xlim(_get_x_lim_graph(parameters, graphs))
    plt.ylim(_get_y_lim_graph(parameters))

    plt.xlabel(parameters.x_label)
    plt.ylabel(parameters.y_label)
    plt.title(parameters.title)


    if not parameters.remove_legend:
        plt.legend(loc=0)


def _manage_derivatives(parameters: PlotParameters, graphs: list[Graph]):
    parameters.derivation_orders.sort()
    if any(order > 3 for order in parameters.derivation_orders):
        LOGGER.info('derivation of higher orders may not be very accurate. The number of points used to compute the derivative will be reduced if necessary. Reduce it further to get more accurate.')

    derivatives = compute_derivatives(parameters, graphs)

    graphs.extend(derivatives)


def _manage_zeros(parameters: PlotParameters, graphs: list[Graph]):
    if parameters.is_integer:
        LOGGER.info('forcing the inputs to be integers may cause to miss some zeros.')

    try:
        compute_and_print_zeros(parameters, graphs)
    except OSError:
        LOGGER.error("error while saving zeros to file '%s'.", parameters.zeros_file)
    except Exception:
        LOGGER.error("error while computing zeros.")


def _manage_integrals(parameters: PlotParameters, graphs: list[Graph]):
    try:
        compute_and_print_integrals(parameters, graphs)
    except OSError:
        LOGGER.error("error while saving integrals to file '%s'.", parameters.zeros_file)
    except Exception:
        LOGGER.error("error while computing integrals")


def _save_data(parameters: PlotParameters, graphs: list[Graph]):
    column_names: list[str] = []
    data: list[list[float]] = []
    # All base graphs have the same x
    base_graphs = [graph for graph in graphs if graph.type == GraphType.BASE]
    if base_graphs:
        column_names.append(parameters.x_label or 'x')
        data.append(base_graphs[0].inputs.tolist())
        for graph in base_graphs:
            column_names.append(graph.expression)
            data.append(graph.values)

    # Add both x and y for every other graph
    for graph in graphs:
        if graph.type == GraphType.BASE:
            continue

        column_names.append(f'x {{{graph.expression}}}')
        column_names.append(graph.expression)

        data.append(graph.inputs.tolist())
        # Force convert back to python list because values can be np array of python list
        data.append(list(graph.values))

    # Equalize the length of each column
    max_column_height = max(map(len, data))
    for index in range(len(data)):
        data[index].extend(['' for _ in range(max_column_height - len(data[index]))])


    try:
        with open(parameters.save_data_path, 'w', encoding='utf-8') as file:
            csvwriter = csv.writer(file, lineterminator='\n')
            csvwriter.writerow(column_names)
            for index in range(max_column_height):
                csvwriter.writerow(column[index] for column in data)
    except OSError:
        LOGGER.error("error while saving data to file '%s'.", parameters.save_data_path)


def _save_figure(parameters: PlotParameters):
    try:
        plt.savefig(parameters.save_figure_path, bbox_inches='tight')
    except OSError:
        LOGGER.error("error while saving figure to file '%s'.", parameters.save_figure_path)


def plot(parameters: PlotParameters) -> None:
    """_summary_ TODO

    Args:
        parameters (PlotParameters): Object containing all the plot parameters.
        The only mandatory attribute is 'expressions' (a list of strings).
        For all other attributes, if they are missing or set to None, the default value will be used.
        Refer to the PlotParameters class for more details.
    """

    set_default_values(parameters)

    _load_functions(parameters)

    retrieve_python_functions(parameters)
    convert_parameters_expression(parameters)
    replace_implicit_variable_multiplication(parameters)

    inputs = _generate_inputs(parameters)
    graphs = _generate_graphs(parameters, inputs)

    if parameters.data_files is not None:
        graphs.extend(read_files(parameters))

    if parameters.regression_expression is not None:
        graphs.extend(compute_regressions(parameters, graphs))

    if not graphs:
        LOGGER.critical('no expression without errors, cannot plot anything.')
        return

    if parameters.derivation_orders is not None:
        _manage_derivatives(parameters, graphs)

    if parameters.zeros_file is not None:
        _manage_zeros(parameters, graphs)

    if parameters.integral_file is not None:
        _manage_integrals(parameters, graphs)

    if parameters.save_data_path is not None:
        _save_data(parameters, graphs)

    _plot_graphs(parameters, graphs)

    if parameters.save_figure_path is not None:
        _save_figure(parameters)

    if not parameters.no_plot:
        plt.show()
