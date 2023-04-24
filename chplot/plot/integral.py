import sys

import numpy as np

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import _round as round
from chplot.plot.utils import Graph, GraphType
from chplot.plot.utils import LOGGER


# See https://en.wikipedia.org/wiki/Trapezoidal_rule for the computation of the integral
def _compute_integral(parameters: PlotParameters, graph: Graph) -> float:
    delta = graph.inputs[1] - graph.inputs[0]
    # use numpy as it's faster even with the conversion
    values = np.nan_to_num(graph.values, copy=True, nan=0)

    integral = sum(values[1:-1]) + (values[0] + values[-1]) / 2
    integral *= delta

    return float(integral)


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
            integral = _compute_integral(parameters, graph)
        except Exception:
            LOGGER.error("error while computing integral for expression '%s'", graph.expression)
            continue

        file.write('\n')
        file.write(f'- ∫f(x)dx = {integral}\n    where f(x) = {graph.expression} on [{round(graph.inputs[0], 3)} ; {round(graph.inputs[-1], 3)}]\n')
        file.write('\n')

    file.write('\n')

    if file is not sys.stdout:
        file.close()
