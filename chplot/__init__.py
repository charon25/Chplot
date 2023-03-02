import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from chplot.rpn import compute_rpn_unsafe
