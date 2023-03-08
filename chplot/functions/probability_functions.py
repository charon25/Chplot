import math

from chplot.functions.utils import FunctionDict


def _norm_pdf(x: float, mu: float, sigma: float) -> float:
    # 2.5066282746310002 = sqrt(2*pi)
    return math.exp(-0.5 * ((x - mu) / sigma)**2) / (sigma * 2.5066282746310002)

def _unit_norm_pdf(x: float) -> float:
    # 2.5066282746310002 = sqrt(2*pi)
    return math.exp(-0.5 * x * x) / 2.5066282746310002

def _norm_cdf(x: float, mu: float, sigma: float) -> float:
    # 1.4142135623730951 = sqrt(2)
    return 0.5 * (1 + math.erf((x - mu) / (sigma * 1.4142135623730951)))

def _unit_norm_cdf(x: float) -> float:
    # 1.4142135623730951 = sqrt(2)
    return 0.5 * (1 + math.erf(x / 1.4142135623730951))


PROBABILITY_FUNCTIONS: FunctionDict = {
    # Normal distribution
    'normpdf': (3, _norm_pdf),
    'unormpdf': (1, _unit_norm_pdf),
    'normcdf': (3, _norm_cdf),
    'unormcdf': (1, _unit_norm_cdf),
}
