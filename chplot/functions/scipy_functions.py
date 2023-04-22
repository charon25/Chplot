import scipy.special

from chplot.functions.utils import FunctionDict, get_functions_from_module, get_renamed_functions_from_module



_SCIPY_SPECIAL_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    (2, 'agm'),
    (1, 'lambertw'),

    (1, 'factorial'), 
    (2, 'binom'),

    (1, 'rgamma'), (1, 'loggamma'),
    (2, 'gammainc'), (2, 'gammaincinv'), (2, 'gammaincc'), (2, 'gammainccinv'),
    (1, 'psi'), (1, 'digamma'),

    (2, 'beta'), (2, 'betaln'), (3, 'betainc'), (3, 'betaincinv'),

    (1, 'erfi'), (1, 'erfinv'),
    (1, 'erfcinv'),

    (1, 'ber'), (1, 'bei'), (1, 'berp'), (1, 'beip'),
    (1, 'ker'), (1, 'kei'), (1, 'kerp'), (1, 'keip'),
    (2, 'jv'), (2, 'yv'), (2, 'kv'), (2, 'iv'),

    (2, 'struve'), (2, 'modstruve'),
    (1, 'itstruve0'), (1, 'it2struve0'), (1, 'itmodstruve0'),

    (3, 'hyperu'), (2, 'hyp0f1'), (3, 'hyp1f1'), (4, 'hyp2f1'),

    (1, 'ellipk'), (2, 'ellipkinc'), (1, 'ellipe'), (2, 'ellipeinc'), (3, 'elliprf'), (2, 'elliprc'), (4, 'elliprj'), (3, 'elliprg'), (3, 'elliprd'),

    (1, 'zeta'),

]

_SCIPY_SPECIAL_MODULE_FUNCTION_RENAMED: tuple[str, int, str] = {
    ('binomial', 2, 'binom'),

    ('sincpi', 1, 'sinc'),

    ('fac', 1, 'factorial'),

    ('besselj', 2, 'jv'), ('bessely', 2, 'yv'), ('besselk', 2, 'kv'), ('besseli', 2, 'iv'),

    ('struveh', 2, 'struve'), ('struvel', 2, 'modstruve'),

    ('hurwitz', 2, 'zeta'), ('hurwitzzeta', 2, 'zeta'),

}

def _fresnels(x: float) -> float:
    return scipy.special.fresnel(x)[0]
def _fresnelc(x: float) -> float:
    return scipy.special.fresnel(x)[1]

def _Ai(x: float) -> float:
    return scipy.special.airy(x)[0]
def _Bi(x: float) -> float:
    return scipy.special.airy(x)[1]
def _Aip(x: float) -> float:
    return scipy.special.airy(x)[2]
def _Bip(x: float) -> float:
    return scipy.special.airy(x)[3]

def _Si(x: float) -> float:
    return scipy.special.sici(x)[0]
def _Ci(x: float) -> float:
    return scipy.special.sici(x)[1]

def _Shi(x: float) -> float:
    return scipy.special.shichi(x)[0]
def _Chi(x: float) -> float:
    return scipy.special.shichi(x)[1]

SCIPY_SPECIAL_FUNCTIONS: FunctionDict = get_functions_from_module(scipy.special, _SCIPY_SPECIAL_MODULE_FUNCTION_NAMES)

SCIPY_SPECIAL_FUNCTIONS.update({
    'fresnels': (1, _fresnels),
    'fresnelc': (1, _fresnelc),
    'Ai': (1, _Ai),
    'Aip': (1, _Aip),
    'Bi': (1, _Bi),
    'Bip': (1, _Bip),
    'Si': (1, _Si),
    'Ci': (1, _Ci),
    'Shi': (1, _Shi),
    'Chi': (1, _Chi),
})

SCIPY_SPECIAL_FUNCTIONS.update(get_renamed_functions_from_module(scipy.special, _SCIPY_SPECIAL_MODULE_FUNCTION_RENAMED))
