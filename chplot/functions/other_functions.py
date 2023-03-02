import math

from chplot.functions.utils import FunctionDict


def _relu(x: float) -> float:
    return x if x > 0 else 0

def _leaky_relu(x: float, a: float) -> float:
    return x if x > 0 else a * x

def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def _sign(x: float) -> float:
    if x < 0:
        return -1
    return 1 if x > 0 else 0

def _lerp(x: float, xa: float, xb: float, ya: float, yb: float) -> float:
    return ya + ((x - xa) / (xb - xa)) * (yb - ya)

def _heaviside(x: float) -> float:
    if x < 0:
        return 0
    return 1 if x > 0 else 0.5

def _sinc(x: float) -> float:
    return math.sin(x) / x

def _norm_sinc(x: float) -> float:
    return math.sin(x / math.pi) / (x * math.pi)

def _rect(x: float) -> float:
    if x < -0.5 or x > 0.5:
        return 0
    return 1

def _triangle(x: float) -> float:
    if x < -1 or x > 1:
        return 0
    return 1 - abs(x)


OTHER_FUNCTIONS: FunctionDict = {
    'relu': (1, _relu),
    'lrelu': (2, _leaky_relu),
    'sigm': (1, _sigmoid),
    'sigmoid': (1, _sigmoid),
    'sign': (1, _sign),
    'sgn': (1, _sign),
    'lerp': (5, _lerp),
    'heaviside': (1, _heaviside),
    'sinc': (1, _sinc),
    'nsinc': (1, _norm_sinc),
    'normsinc': (1, _norm_sinc),
    'rect': (1, _rect),
    'triangle': (1, _triangle),
    'tri': (1, _triangle),
    'abs': (1, abs),
    'min': (2, min),
    'min3': (3, min),
    'min4': (4, min),
    'max': (2, max),
    'max3': (3, max),
    'max4': (4, max),
}
