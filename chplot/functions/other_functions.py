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

def _lerp(x: float, x_min: float, x_max: float, y_min: float, y_max: float) -> float:
    return y_min + ((x - x_min) / (x_max - x_min)) * (y_max - y_min)

def _lerpt(t: float, _min: float, _max: float) -> float:
    return _max + t * (_max - _min)

def _heaviside(x: float) -> float:
    if x < 0:
        return 0
    return 1 if x > 0 else 0.5

def _rect(x: float) -> float:
    if x < -0.5 or x > 0.5:
        return 0
    return 1

def _triangle(x: float) -> float:
    if x < -1 or x > 1:
        return 0
    return 1 - abs(x)

def _if(x: float, _true: float, _false: float) -> float:
    return _true if x >= 0 else _false

def _ifn(x: float, _true: float, _false: float) -> float:
    return _true if x <= 0 else _false

def _ifz(x: float, _true: float, _false: float) -> float:
    return _true if x == 0 else _false

def _in(x: float, lower: float, upper: float, _true: float, _false: float) -> float:
    return _true if lower <= x <= upper else _false

def _out(x: float, lower: float, upper: float, _true: float, _false: float) -> float:
    return _false if lower <= x <= upper else _true


OTHER_FUNCTIONS: FunctionDict = {
    'relu': (1, _relu),
    'lrelu': (2, _leaky_relu),

    'sigm': (1, _sigmoid),
    'sigmoid': (1, _sigmoid),

    'sign': (1, _sign),
    'sgn': (1, _sign),

    'lerp': (5, _lerp),
    'lerpt': (3, _lerpt),

    'heaviside': (1, _heaviside),
    'ramp': (1, _relu),
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

    'if': (3, _if),
    'ifn': (3, _ifn),
    'ifz': (3, _ifz),
    'in': (5, _in),
    'out': (5, _out),
}
