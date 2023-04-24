"""
Chplot is a Python >= 3.9 module to plot any arbitrary mathematical expressions as well as data series from files, and compute its derivatives and integrals, where it equals zero, linear and non-linear regressions, and much more !

It is best used from the CLI, with 'python -m chplot', but it can also be used from a Python script:

```
import chplot

parameters = chplot.PlotParameters()
chplot.plot(parameters)
```

Check all the documentation on the github repo (https://github.com/charon25/Chplot).

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
