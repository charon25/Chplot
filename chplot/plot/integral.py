import logging
import math
import numpy as np
import sys

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph


logger = logging.getLogger(__name__)


# See https://en.wikipedia.org/wiki/Trapezoidal_rule for the computation of the integral
# and http://isdl.cau.ac.kr/education.data/numerical.analysis/Lecture17.pdf for the computation of the second derivative needed for the error
def _compute_integral(parameters: PlotParameters, graph: Graph) -> tuple[float, float]:
    delta = graph.inputs[1] - graph.inputs[0]
    # use numpy as it's faster even with the conversion
    np_values = np.nan_to_num(graph.values, copy=True, nan=0)

    integral = sum(np_values[1:-1]) + (np_values[0] + np_values[-1]) / 2
    integral *= delta

    unscaled_second_derivative = -np_values[3:] + 4 * np_values[2:-1] - 5 * np_values[1:-2] + 2 * np_values[:-3]
    second_derivative_abs_maximum = np.max(np.abs(unscaled_second_derivative)) / (delta * delta)

    abs_error = second_derivative_abs_maximum * ((graph.inputs[-1] - graph.inputs[1]) ** 3) / (12 * (parameters.n_points ** 2))

    return (float(integral), float(abs_error))


def compute_and_print_integrals(parameters: PlotParameters, graphs: list[Graph]):
    # print to stdout
    if parameters.integral_file == 0:
        file = sys.stdout
    else:
        file = open(parameters.integral_file, 'w', encoding='utf-8')

    file.write('\nNote that the more points, the smallest the error and that floating point numbers may introduce errors.\n')
    file.write(f'The integral on the interval [{round(parameters.x_lim[0], 3)} ; {round(parameters.x_lim[1], 3)}] of the function{"s" if len(graphs) > 1 else ""}...\n\n')
    for graph in graphs:
        expression = graph[0]
        try:
            integral, abs_error = _compute_integral(parameters, graph)
            max_decimal_places = abs(math.floor(1 + math.log10(abs_error)))
        except Exception:
            logger.error("error while computing integral for expression '%s'", expression)
            continue

        file.write(f' f(x) = {expression} is {round(integral, max_decimal_places)} ± {abs_error:.2e}...\n')
        file.write('\n')

    file.write('\n')

    if file is not sys.stdout:
        file.close()
