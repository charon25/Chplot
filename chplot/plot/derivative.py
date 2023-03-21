

import numpy as np

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph



def _get_size_reduction(n: int) -> int:
    """Return the size reduction of each side of the output vector after differentiation of order n.
    This mean it should be doubled to get the total shrinkage."""
    q, r = divmod(n, 6)
    reduction = 5 * q
    if r == 0:
        return reduction
    elif r == 5:
        return reduction + 5
    return reduction + 4


# All the coefficients below are taken from https://en.wikipedia.org/wiki/Finite_difference_coefficient

def _get_first_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (1/280 * f[0:-8] - 4/105 * f[1:-7] + 1/5 * f[2:-6] - 4/5 * f[3:-5] + 4/5 * f[5:-3] - 1/5 * f[6:-2] + 4/105 * f[7:-1] - 1/280 * f[8:]) / h

def _get_second_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (-1/560 * f[0:-8] + 8/315 * f[1:-7] - 1/5 * f[2:-6] + 8/5 * f[3:-5] - 205/72 * f[4:-4] + 8/5 * f[5:-3] - 1/5 * f[6:-2] + 8/315 * f[7:-1] - 1/560 * f[8:]) / (h * h)

def _get_third_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (-7/240 * f[0:-8] + 3/10 * f[1:-7] - 169/120 * f[2:-6] + 61/30 * f[3:-5] - 61/30 * f[5:-3] + 169/120 * f[6:-2] - 3/10 * f[7:-1] + 7/240 * f[8:]) / (h ** 3)

def _get_fourth_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (7/240 * f[0:-8] - 2/5 * f[1:-7] + 169/60 * f[2:-6] - 122/15 * f[3:-5] + 91/8 * f[4:-4] - 122/15 * f[5:-3] + 169/60 * f[6:-2] - 2/5 * f[7:-1] + 7/240 * f[8:]) / (h ** 4)

def _get_fifth_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (-13/288 * f[0:-10] + 19/36 * f[1:-9] - 87/32 * f[2:-8] + 13/2 * f[3:-7] - 323/48 * f[4:-6] + 323/48 * f[6:-4] - 13/2 * f[7:-3] + 87/32 * f[8:-2] - 19/36 * f[9:-1] + 13/288 * f[10:]) / (h ** 5)

def _get_sixth_derivative(f: np.ndarray, h: float) -> np.ndarray:
    return (13/240 * f[0:-10] - 19/24 * f[1:-9] + 87/16 * f[2:-8] - 39/2 * f[3:-7] + 323/8 * f[4:-6] - 1023/20 * f[5:-5] + 323/8 * f[6:-4] - 39/2 * f[7:-3] + 87/16 * f[8:-2] - 19/24 * f[9:-1] + 13/240 * f[10:]) / (h ** 6)


def _get_nth_derivative(f: np.ndarray, h: float, n: int) -> np.ndarray:
    """To derivate the function n=4q+r times, get the fourth derivative q times then get the r-th derivative of this.
    Note that the array f will shrink after every derivative. It will lose (3q+a) elements on each side, where a=0 if r=0, a=2 if r=1,2 and a=3 if r=3"""
    q, r = divmod(n, 6)
    for _ in range(q):
        f = _get_sixth_derivative(f, h)

    if r == 1:
        f = _get_first_derivative(f, h)
    elif r == 2:
        f = _get_second_derivative(f, h)
    elif r == 3:
        f = _get_third_derivative(f, h)
    elif r == 4:
        f = _get_fourth_derivative(f, h)
    elif r == 5:
        f = _get_fifth_derivative(f, h)

    return f


def compute_derivatives(parameters: PlotParameters, graphs: list[Graph]) -> list[Graph]:
    derivatives: list[Graph] = []
    for graph in graphs:
        h = graph.inputs[1] - graph.inputs[0]
        for order in parameters.derivation_orders:
            shrinkage = _get_size_reduction(order)
            derivative_graph = Graph(
                inputs=graph.inputs[shrinkage:-shrinkage],
                expression=f'd{order}/dx{order} * {graph.expression}',
                rpn=None,
                values=_get_nth_derivative(graph.values, h, order)
            )
            derivatives.append(derivative_graph)
    pass
