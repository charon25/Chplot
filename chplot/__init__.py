"""
TODO
"""

import logging
import sys
import warnings

import numpy as np

from chplot.rpn import compute_rpn_list, compute_rpn_unsafe, get_rpn_errors
from chplot.plot import plot, plottable
from chplot.plot.plot_parameters import PlotParameters, set_default_values

np.seterr('raise')

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='[%(name)s] %(levelname)s: %(message)s'
)

warnings.filterwarnings("ignore")
