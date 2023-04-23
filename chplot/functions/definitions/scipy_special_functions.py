from scipy.special import *

def _fresnels(x: float) -> float:
    return fresnel(x)[0]
def _fresnelc(x: float) -> float:
    return fresnel(x)[1]

def _Ai(x: float) -> float:
    return airy(x)[0]
def _Aip(x: float) -> float:
    return airy(x)[1]
def _Bi(x: float) -> float:
    return airy(x)[2]
def _Bip(x: float) -> float:
    return airy(x)[3]

def _eAi(x: float) -> float:
    return airye(x)[0]
def _eAip(x: float) -> float:
    return airye(x)[1]
def _eBi(x: float) -> float:
    return airye(x)[2]
def _eBip(x: float) -> float:
    return airye(x)[3]

def _Si(x: float) -> float:
    return sici(x)[0]
def _Ci(x: float) -> float:
    return sici(x)[1]

def _Shi(x: float) -> float:
    return shichi(x)[0]
def _Chi(x: float) -> float:
    return shichi(x)[1]
