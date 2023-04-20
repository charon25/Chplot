import mpmath

from chplot.functions.utils import FunctionDict, get_functions_from_module, get_renamed_functions_from_module


_MPMATH_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    (1, 'sec'), (1, 'csc'), (1, 'cot'),
    (1, 'asec'), (1, 'acsc'), (1, 'acot'),
    (1, 'cospi'), (1, 'cospi'),
    (1, 'sinc'),
    (1, 'sech'), (1, 'csch'), (1, 'coth'),
    (1, 'asech'), (1, 'acsch'), (1, 'acoth'),

    (1, 'fac2'),
    (1, 'rf'), (1, 'ff'),
    (1, 'superfac'), (1, 'hyperfac'), (1, 'barnesg'),
    (1, 'harmonic'),

    (1, 'li'),

    (2, 'angerj'), (2, 'webere'),
    (3, 'lommels1'), (3, 'lommels2'),
    (1, 'scorergi'), (1, 'scorerhi'),
    (3, 'coulombf'), (3, 'coulombg'), (2, 'coulombc'),
    (3, 'whitm'), (3, 'whitw'),
    (2, 'pcfd'), (2, 'pcfu'), (2, 'pcfv'), (2, 'pcfw'),

    (2, 'legendre'), (3, 'legenp'), (3, 'legenq'),
    (2, 'chebyt'), (2, 'chebyu'),
    (4, 'jacobi'), (3, 'gegenbauer'), (2, 'hermite'), (3, 'laguerre'),

    (4, 'hyp1f2'), (3, 'hyp2f0'), (5, 'hyp2f3'), (6, 'hyp3f2'),

    (2, 'ellipf'), (3, 'ellippi'),

    (1, 'altzeta'), (1, 'stieltjes'), (1, 'siegelz'), (1, 'siegeltheta'),
    (1, 'backlunds'), (3, 'lerchphi'),
    (2, 'polylog'), (2, 'clsin'), (2, 'clcos'), (2, 'polyexp'),
    (1, 'primezeta'), (1, 'secondzeta'),

    (1, 'fib'), (1, 'fibonacci'),
    (1, 'primepi'), (1, 'riemannr'),
]

_MPMATH_MODULE_FUNCTION_RENAMED: tuple[str, int, str] = {
    ('betainc2', 4, 'betainc'),

    ('W', 1, 'lambertw'),
    ('Ei', 1, 'ei'),

    ('normsinc', 1, 'sincpi'), ('nsinc', 1, 'sincpi'),

    ('gammainc2', 3, 'gammainc'),

    ('hurwitz', 2, 'zeta'), ('hurwitzzeta', 2, 'zeta'), ('eta', 1, 'altzeta'), ('nzetazeros', 1, 'nzeros')

}


def _Li(x: float) -> float:
    return mpmath.li(x, offset=True)

MPMATH_FUNCTIONS: FunctionDict = get_functions_from_module(mpmath, _MPMATH_MODULE_FUNCTION_NAMES)

MPMATH_FUNCTIONS.update({
    'Li': (1, _Li),
})

MPMATH_FUNCTIONS.update(get_renamed_functions_from_module(mpmath, _MPMATH_MODULE_FUNCTION_RENAMED))
