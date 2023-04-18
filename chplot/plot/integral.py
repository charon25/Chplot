import math
import numpy as np
import sys

from chplot.plot.derivative import _get_second_derivative
from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import _round as round
from chplot.plot.utils import Graph, GraphType
from chplot.plot.utils import LOGGER


# See https://en.wikipedia.org/wiki/Trapezoidal_rule for the computation of the integral
def _compute_integral(parameters: PlotParameters, graph: Graph) -> tuple[float, float]:
    delta = graph.inputs[1] - graph.inputs[0]
    # use numpy as it's faster even with the conversion
    values = np.nan_to_num(graph.values, copy=True, nan=0)

    integral = sum(values[1:-1]) + (values[0] + values[-1]) / 2
    integral *= delta

    second_derivative_abs_maximum = np.max(np.abs(_get_second_derivative(values, delta)))

    abs_error = second_derivative_abs_maximum * ((graph.inputs[-1] - graph.inputs[0]) ** 3) / (12 * (parameters.n_points ** 2))

    return (float(integral), float(abs_error))


def compute_and_print_integrals(parameters: PlotParameters, graphs: list[Graph]):
    # print to stdout
    if parameters.integral_file == 0:
        file = sys.stdout
    else:
        file = open(parameters.integral_file, 'w', encoding='utf-8')

    file.write('\n===== INTEGRALS OF THE FUNCTIONS =====\n')
    file.write('Note that the more points, the smallest the error and that floating point numbers may introduce errors. Furthermore, discontinuous functions may indicate really huge error margins.\n')

    if any(graph.type == GraphType.DERIVATIVE for graph in graphs):
        file.write('The x-axis limits on derivatives are slightly tighter because of the algorithm used. This may be counteracted by adding more points.\n')

    # file.write(f'\nThe integral of the function{"s" if len(graphs) > 1 else ""}...\n\n')
    for graph in graphs:
        try:
            integral, abs_error = _compute_integral(parameters, graph)
            max_decimal_places = abs(math.floor(1 + math.log10(abs_error)))
        except Exception:
            LOGGER.error("error while computing integral for expression '%s'", graph.expression)
            continue

        file.write('\n')
        file.write(f'- ∫f(x)dx = {round(integral, max_decimal_places)} ± {abs_error:.2e}\n    where f(x) = {graph.expression} on [{round(graph.inputs[0], 3)} ; {round(graph.inputs[-1], 3)}]\n')
        file.write('\n')

    file.write('\n')

    if file is not sys.stdout:
        file.close()
