import math

from chplot import plottable


@plottable(1)
def frac(x: float) -> float:
    return x % 1

@plottable(arg_count=1)
def is_prime(x: float) -> bool:
    n = int(x)
    for k in range(2, math.isqrt(n) + 1):
        if n % k == 0:
            return False
    return True

@plottable(arg_count=2)
def rnd(x: float, d: float) -> float:
    d = int(d)
    return round(x, d)
