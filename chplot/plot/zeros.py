import math
import numpy as np

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph, GraphList, ZerosList
from chplot.rpn import compute_rpn_unsafe


TARGET_ERROR = 1e-15
MAX_ITERATIONS = 200


def _compute_simple_zero(parameters: PlotParameters, inputs: np.ndarray, rpn_tokens: list[str], zero_index: int) -> float:
    """Given one index where the sign changes, get the closest float value to the real zero of the function.
    Can only be accurate if the function is continuous."""
    xa, xb = map(float, inputs[zero_index:zero_index + 2]) # convert to real float for the rpn compute algorithm
    fa = compute_rpn_unsafe(rpn_tokens, xa, variable=parameters.variable)
    
    it = 0
    while it < MAX_ITERATIONS and xb - xa > TARGET_ERROR:
        xm = (xa + xb) / 2
        fm = compute_rpn_unsafe(rpn_tokens, xm, variable=parameters.variable)
        if fa * fm > 0:
            xa = xm
            fa = fm
        elif fa * fm < 0:
            xb = xm
        else:
            return xm

        it += 1

    return xa


def _compute_zero_zone(parameters: PlotParameters, inputs: np.ndarray, rpn_tokens: list[str], zone_start: int, zone_end: int, outputs: list[float]) -> tuple[float, float]:
    """Given an interval where the function is always zero, get the closest float value to the real start and end of this interval.
    Can only be accurate if the function is continuous."""
    # if the zone is at the start of the input, do not compute its start further as we do not go outside the x range
    if zone_start == 0:
        compute_start = False
        start_xa = float(inputs[0])
        start_xb = start_xa
    else:
        compute_start = True
        # get the last x where f(x) != 0 then the first x where f(x) = 0
        start_xa, start_xb = map(float, inputs[zone_start - 1:zone_start + 1]) # convert to real float for the rpn compute algorithm

    # if the zone is at the end of the input, do not compute its end further as we do not go outside the x range
    if zone_end == len(inputs) - 1:
        compute_end = False
        end_xa = float(inputs[-1])
        end_xb = end_xa
    else:
        compute_end = True
        # get the first x where f(x) != 0 then the last x where f(x) = 0
        end_xa, end_xb = map(float, inputs[zone_end:zone_end + 2])

    it = 0
    while (it < MAX_ITERATIONS) and ((start_xb - start_xa > TARGET_ERROR) or (end_xb - end_xa > TARGET_ERROR)):
        if compute_start:
            start_xm = (start_xa + start_xb) / 2
            if compute_rpn_unsafe(rpn_tokens, start_xm, variable=parameters.variable) == 0:
                start_xb = start_xm
            else:
                start_xa = start_xm

        if compute_end:
            end_xm = (end_xa + end_xb) / 2
            if compute_rpn_unsafe(rpn_tokens, end_xm, variable=parameters.variable) == 0:
                end_xa = end_xm
            else:
                end_xb = end_xm

        it += 1

    return (start_xa, end_xa)


def _compute_zeros(parameters: PlotParameters, inputs: np.ndarray, graph: Graph) -> ZerosList:
    _, rpn, outputs = graph

    simple_zeros: list[float] = []  # Values of x where graph[x] = 0
    simple_zeros_indexes: list[int] = []    # Indexes where to compute simple zeros
    zero_zones_indexes: list[int] = []      # Indexes of zero "zones", always by two (start and end)

    for index, (y1, y2) in enumerate(zip(outputs, outputs[1:])):
        # No point to do anything is one is nan
        if math.isnan(y1) or math.isnan(y2):
            continue
        # Same sign, no zero here
        if y1 * y2 > 0:
            continue
        # Opposite sign, there is a simple zero
        elif y1 * y2 < 0:
            simple_zeros_indexes.append(index)
        elif y1 * y2 == 0:
            # Start of a zero "zone" only we are not at the end, else a simple zero we cannot compute further
            if y1 != 0:
                if index == len(inputs) - 2:
                    simple_zeros.append(inputs[index + 1])
                else:
                    zero_zones_indexes.append(index + 1)
            # Either we're at the beginning and it is a simple zero we cannot compute further,
            # or it's either the end of the current zone or just a simple zero is the zone has length 1
            elif y2 != 0:
                if index == 0:
                    simple_zeros.append(inputs[0])
                else:
                    # We got something like 1, 0, 1 or -1, 0, 1 so we got a simple zero already computed
                    if index == zero_zones_indexes[-1]:
                        zero_zones_indexes.pop()
                        simple_zeros.append(inputs[index])
                    else:
                        zero_zones_indexes.append(index)
            # If we're at the beginning, it's start of a zero zone, else nothing
            else:
                if index == 0:
                    zero_zones_indexes.append(0)

    # the last zero zone goes until the end, so it needs to be closed
    if len(zero_zones_indexes) % 2 == 1:
        zero_zones_indexes.append(len(inputs) - 1)

    rpn_tokens = rpn.split(' ')
    simple_zeros.extend(_compute_simple_zero(parameters, inputs, rpn_tokens, zero_index) for zero_index in simple_zeros_indexes)

    all_zeros: ZerosList = [(zero_x, None) for zero_x in simple_zeros]
    all_zeros.extend(
        _compute_zero_zone(
            parameters, inputs, rpn_tokens,
            zero_zones_indexes[index], zero_zones_indexes[index + 1], outputs
        ) for index in range(0, len(zero_zones_indexes), 2)
    )

    return sorted(all_zeros)



def compute_and_print_zeros(parameters: PlotParameters, inputs: np.ndarray, graphs: GraphList):
    pass
