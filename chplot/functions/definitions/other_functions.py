import math


def relu(x: float) -> float:
    return x if x > 0 else 0

def leaky_relu(x: float, a: float) -> float:
    return x if x > 0 else a * x

def sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def sign(x: float) -> float:
    if x < 0:
        return -1
    return 1 if x > 0 else 0

def lerp(x: float, x_min: float, x_max: float, y_min: float, y_max: float) -> float:
    return y_min + ((x - x_min) / (x_max - x_min)) * (y_max - y_min)

def lerpt(t: float, _min: float, _max: float) -> float:
    return _max + t * (_max - _min)

def heaviside(x: float) -> float:
    if x < 0:
        return 0
    return 1 if x > 0 else 0.5

def rect(x: float) -> float:
    if x < -0.5 or x > 0.5:
        return 0
    return 1

def triangle(x: float) -> float:
    if x < -1 or x > 1:
        return 0
    return 1 - abs(x)

def sawtooth(x: float) -> float:
    return 2 * ((x - 1/2) % 1) - 1

def squarewave(x: float) -> float:
    m = x % 1
    if m in (0, 0.5):
        return 0.5
    if m < 0.5:
        return 1
    return 0

def trianglewave(x: float) -> float:
    m = x % 1
    if m < 0.25:
        return 4 * m
    if m < 0.75:
        return 2 - 4 * m
    return 4 * m - 4

def _if(x: float, _true: float, _false: float) -> float:
    return _true if x >= 0 else _false

def ifn(x: float, _true: float, _false: float) -> float:
    return _true if x <= 0 else _false

def ifz(x: float, _true: float, _false: float) -> float:
    return _true if x == 0 else _false

def _in(x: float, lower: float, upper: float, _true: float, _false: float) -> float:
    return _true if lower <= x <= upper else _false

def out(x: float, lower: float, upper: float, _true: float, _false: float) -> float:
    return _false if lower <= x <= upper else _true
