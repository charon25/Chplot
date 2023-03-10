import logging
import math

import scipy.stats

from chplot.functions.utils import FunctionDict


logger = logging.getLogger(__name__)


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

def _uniform_pdf(x: float, a: float, b: float) -> float:
    return 1 / (b - a) if a <= x <= b else 0

def _uniform_cdf(x: float, a: float, b: float) -> float:
    if a <= x <= b:
        return (x - a) / (b - a)
    return 0 if x < a else 1

def _expon_pdf(x: float, lamb: float) -> float:
    return lamb * math.exp(-lamb * x) if x >= 0 else 0

def _expon_cdf(x: float, lamb: float) -> float:
    return 1 - math.exp(-lamb * x) if x >= 0 else 0

def _cauchy_pdf(x: float, x0: float, gamma: float) -> float:
    return 1 / (math.pi * gamma * (1 + ((x - x0) / gamma) ** 2))

def _cauchy_cdf(x: float, x0: float, gamma: float) -> float:
    # 0.3183098861837907 = 1 / pi
    return 0.5 + 0.3183098861837907 * math.atan((x - x0) / gamma)

def _student_pdf(x: float, nu: float) -> float:
    return scipy.stats.t.pdf(x, nu)

def _student_cdf(x: float, nu: float) -> float:
    return scipy.stats.t.cdf(x, nu)

def _beta_pdf(x: float, alpha: float, beta: float) -> float:
    return scipy.stats.beta.pdf(x, alpha, beta)

def _beta_cdf(x: float, alpha: float, beta: float) -> float:
    return scipy.stats.beta.cdf(x, alpha, beta)

def _chi2_pdf(x: float, k: float) -> float:
    return scipy.stats.chi2.pdf(x, k)

def _chi2_cdf(x: float, k: float) -> float:
    return scipy.stats.chi2.cdf(x, k)

# The scale is defined from https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html#scipy.stats.gamma
def _gamma_pdf(x: float, alpha: float, beta: float) -> float:
    return scipy.stats.gamma.pdf(x, alpha, scale=1/beta)

def _gamma_cdf(x: float, alpha: float, beta: float) -> float:
    return scipy.stats.gamma.cdf(x, alpha, scale=1/beta)


PROBABILITY_FUNCTIONS: FunctionDict = {
    # Normal distribution
    'normpdf': (3, _norm_pdf),
    'unormpdf': (1, _unit_norm_pdf),
    'normcdf': (3, _norm_cdf),
    'unormcdf': (1, _unit_norm_cdf),
    # Uniform distribution
    'uniformpdf': (3, _uniform_pdf),
    'uniformcdf': (3, _uniform_cdf),
    # Exponential distribution
    'exponpdf': (2, _expon_pdf),
    'exponcdf': (2, _expon_cdf),
    # Student's t distribution
    'studentpdf': (2, _student_pdf),
    'studentcdf': (2, _student_cdf),
    # Beta distribution
    'betapdf': (3, _beta_pdf),
    'betacdf': (3, _beta_cdf),
    # Chi squared distribution
    'chi2pdf': (2, _chi2_pdf),
    'khi2pdf': (2, _chi2_pdf),
    'chi2cdf': (2, _chi2_cdf),
    'khi2cdf': (2, _chi2_cdf),
    # Gamma distribution
    'gammapdf': (3, _gamma_pdf),
    'gammacdf': (3, _gamma_cdf),
    # Cauchy distribution
    'cauchypdf': (3, _cauchy_pdf),
    'cauchycdf': (3, _cauchy_cdf),

}
