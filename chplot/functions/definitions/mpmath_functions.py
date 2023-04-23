from mpmath import *


def _Li(x: float) -> float:
    return li(x, offset=True)
