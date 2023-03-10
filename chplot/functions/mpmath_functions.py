import logging

import mpmath

from chplot.functions.utils import FunctionDict, get_functions_from_module, get_renamed_functions_from_module


logger = logging.getLogger(__name__)


_MPMATH_MODULE_FUNCTION_NAMES: tuple[int, str] = [
    (1, 'lambertw'),
    (2, 'agm'),

    (1, 'sec'), (1, 'csc'), (1, 'cot'),
    (1, 'asec'), (1, 'acsc'), (1, 'acot'),
    (1, 'cospi'), (1, 'cospi'),
    (1, 'sinc'), (1, 'sincpi'),
    (1, 'sech'), (1, 'csch'), (1, 'coth'),
    (1, 'asech'), (1, 'acsch'), (1, 'acoth'),

    (1, 'factorial'), (1, 'fac'), (1, 'fac2'),
    (2, 'binomial'),    
    (1, 'rgamma'), (1, 'loggamma'), (3, 'gammainc'),
    (1, 'rf'), (1, 'ff'),
    (2, 'beta'), (4, 'betainc'),
    (1, 'superfac'), (1, 'hyperfac'), (1, 'barnesg'),
    (1, 'digamma'),
    (1, 'harmonic'),

    (3, 'gammainc'),
    (1, 'li'),
    (1, 'erfi'), (1, 'erfinv'),
    (3, 'npdf'), (3, 'ncdf'),
    (1, 'fresnels'), (1, 'fresnelc'),

    (2, 'besselj'), (2, 'bessely'), (2, 'besseli'), (2, 'besselk'),
    (2, 'ber'), (2, 'bei'), (2, 'ker'), (2, 'kei'),
    (2, 'struveh'), (2, 'struvel'),
    (2, 'angerj'), (2, 'webere'),
    (3, 'lommels1'), (3, 'lommels2'),
    (2, 'airyai'), (2, 'airybi'),
    (1, 'scorergi'), (1, 'scorerhi'),
    (3, 'coulombf'), (3, 'coulombg'), (2, 'coulombc'),
    (3, 'hyperu'), (3, 'whitm'), (3, 'whitw'),
    (2, 'pcfd'), (2, 'pcfu'), (2, 'pcfv'), (2, 'pcfw'),

    (2, 'legendre'), (3, 'legenp'), (3, 'legenq'),
    (2, 'chebyt'), (2, 'chebyu'),
    (4, 'jacobi'), (3, 'gegenbauer'), (2, 'hermite'), (3, 'laguerre'),

    (2, 'hyp0f1'), (3, 'hyp1f1'), (4, 'hyp1f2'), (3, 'hyp2f0'), (4, 'hyp2f1'), (5, 'hyp2f3'), (6, 'hyp3f2'),

    (2, 'ellipk'), (2, 'ellipf'), (2, 'ellipe'), (3, 'ellippi'), (3, 'elliprf'), (2, 'elliprc'), (4, 'elliprj'), (3, 'elliprd'), (3, 'elliprg'),

    (1, 'zeta'), (1, 'altzeta'), (1, 'stieltjes'), (1, 'siegelz'), (1, 'siegeltheta'),
    (1, 'backlunds'), (3, 'lerchphi'),
    (2, 'polylog'), (2, 'clsin'), (2, 'clcos'), (2, 'polyexp'),
    (1, 'primezeta'), (1, 'secondzeta'), 

    (1, 'fib'), (1, 'fibonacci'),
    (1, 'primepi'), (1, 'riemannr'),
]
_MPMATH_MODULE_FUNCTION_RENAMED: tuple[str, int, str] = {
    ('betainc0', 4, 'betainc'),

    ('W', 1, 'lambertw'),
    ('Ei', 1, 'ei'),
    ('Ci', 1, 'ci'), ('Si', 1, 'si'),
    ('Chi', 1, 'chi'), ('Shi', 1, 'shi'),

    ('normsinc', 1, 'sincpi'), ('nsinc', 1, 'sincpi'),

    ('hurwitz', 2, 'zeta'), ('hurwitzzeta', 2, 'zeta'), ('eta', 1, 'altzeta'), ('nzetazeros', 1, 'nzeros')

}


def _Li(x: float) -> float:
    return mpmath.li(x, offset=True)

def _psi(x: float) -> float:
    return mpmath.psi(0, x)

MPMATH_FUNCTIONS: FunctionDict = get_functions_from_module(mpmath, _MPMATH_MODULE_FUNCTION_NAMES)

MPMATH_FUNCTIONS.update({
    'Li': (1, _Li),
    'psi': (1, _psi),
})

MPMATH_FUNCTIONS.update(get_renamed_functions_from_module(mpmath, _MPMATH_MODULE_FUNCTION_RENAMED))
