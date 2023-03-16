import logging
import math
import numpy as np
import sys

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph, GraphList


logger = logging.getLogger(__name__)


# See https://en.wikipedia.org/wiki/Trapezoidal_rule for the computation of the integral
# and http://isdl.cau.ac.kr/education.data/numerical.analysis/Lecture17.pdf for the computation of the second derivative needed for the error
def _compute_integral(parameters: PlotParameters, inputs: np.ndarray, graph: Graph) -> tuple[float, float]:
    _, _, outputs = graph
    delta = inputs[1] - inputs[0]
    # use numpy as it's faster even with the conversion
    np_outputs = np.nan_to_num(outputs, copy=True, nan=0)

    integral = sum(np_outputs[1:-1]) + (np_outputs[0] + np_outputs[-1]) / 2
    integral *= delta

    unscaled_second_derivative = -np_outputs[3:] + 4 * np_outputs[2:-1] - 5 * np_outputs[1:-2] + 2 * np_outputs[:-3]
    second_derivative_abs_maximum = np.max(np.abs(unscaled_second_derivative)) / (delta * delta)

    abs_error = second_derivative_abs_maximum * ((inputs[-1] - inputs[1]) ** 3) / (12 * (parameters.n_points ** 2))

    return (float(integral), float(abs_error))


def compute_and_print_integrals(parameters: PlotParameters, inputs: np.ndarray, graphs: GraphList):
    # print to stdout
    if parameters.integral_file == 0:
        file = sys.stdout
    else:
        file = open(parameters.zeros_file, 'w', encoding='utf-8')

    file.write('\nNote that the more points, the smallest the error and that floating point numbers may introduce errors.\n')
    file.write(f'The integral on the interval [{round(parameters.x_lim[0], 3)} ; {round(parameters.x_lim[1], 3)}] of the function{"s" if len(graphs) > 1 else ""}...\n\n')
    for graph in graphs:
        expression = graph[0]
        try:
            integral, abs_error = _compute_integral(parameters, inputs, graph)
            max_decimal_places = abs(math.floor(1 + math.log10(abs_error)))
        except Exception:
            logger.error("error while computing integral for expression '%s'", expression)
            continue

        file.write(f' f(x) = {expression} is {round(integral, max_decimal_places)} ± {abs_error:.2e}...\n')
        file.write('\n')

    file.write('\n')

    if file is not sys.stdout:
        file.close()
