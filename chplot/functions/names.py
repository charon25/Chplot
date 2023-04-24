from chplot.functions.utils import FunctionNames


MATH_FUNCTION_NAMES: FunctionNames = [
    ('cos', 1, None), ('sin', 1, None), ('tan', 1, None),
    ('acos', 1, None), ('asin', 1, None), ('atan', 1, None), ('atan2', 2, None),

    ('cosh', 1, None), ('sinh', 1, None), ('tanh', 1, None),
    ('acosh', 1, None), ('asinh', 1, None), ('atanh', 1, None),

    ('sqrt', 1, None), ('cbrt', 1, None),

    ('ceil', 1, None), ('floor', 1, None),

    ('degrees', 1, None), ('radians', 1, None),

    ('erf', 1, None), ('erfc', 1, None),

    ('exp', 1, None), ('expm1', 1, None),
    ('log', 1, None), ('ln', 1, 'log'), ('log10', 1, None), ('log1p', 1, None), ('log2', 1, None),

    ('gamma', 1, None), ('lgamma', 1, None), ('lngamma', 1, 'lgamma'),

    ('fmod', 2, None), ('remainder', 2, None),

    ('hypot', 2, None), ('dist', 4, '_dist'),
    ('copysign', 2, None),
    ('trunc', 1, None)
]


SCIPY_SPECIAL_FUNCTION_NAMES: FunctionNames = [
    ('agm', 2, None),
    ('lambertw', 1, None), ('W', 1, 'lambertw'), ('lambert', 1, 'lambertw'),

    ('factorial', 1, None), ('fac', 1, 'factorial'),
    ('binom', 2, None), ('binomial', 2, 'binom'),

    ('rgamma', 1, None), ('loggamma', 1, None),
    ('gammainc', 2, None), ('gammaincinv', 2, None), ('gammaincc', 2, None), ('gammainccinv', 2, None),
    ('psi', 1, None), ('digamma', 1, None),

    ('beta', 2, None), ('betaln', 2, None), ('betainc', 3, None), ('betaincinv', 3, None),

    ('erfi', 1, None), ('erfinv', 1, None),
    ('erfcinv', 1, None),

    ('ber', 1, None), ('bei', 1, None), ('berp', 1, None), ('beip', 1, None),
    ('ker', 1, None), ('kei', 1, None), ('kerp', 1, None), ('keip', 1, None),
    ('jv', 2, None), ('yv', 2, None), ('kv', 2, None), ('iv', 2, None),
    ('besselj', 2, 'jv'), ('bessely', 2, 'yv'), ('besselk', 2, 'kv'), ('besseli', 2, 'iv'),

    ('struve', 2, None), ('modstruve', 2, None),
    ('itstruve0', 1, None), ('it2struve0', 1, None), ('itmodstruve0', 1, None),

    ('hyperu', 3, None), ('hyp0f1', 2, None), ('hyp1f1', 3, None), ('hyp2f1', 4, None),

    ('ellipk', 1, None), ('ellipkinc', 2, None), ('ellipe', 1, None), ('ellipeinc', 2, None), ('elliprf', 3, None), ('elliprc', 2, None), ('elliprj', 4, None), ('elliprg', 3, None), ('elliprd', 3, None),

    ('zeta', 1, None), ('hurwitz', 2, 'zeta'), ('hurwitzzeta', 2, 'zeta'),

    ('sincpi', 1, 'sinc'),

    ('struveh', 2, 'struve'), ('struvel', 2, 'modstruve'),

    ('fresnels', 1, '_fresnels'), ('fresnelc', 1, '_fresnelc'),

    ('Ai', 1, '_Ai'), ('Aip', 1, '_Aip'), ('Bi', 1, '_Bi'), ('Bip', 1, '_Bip'),
    ('eAi', 1, '_eAi'), ('eAip', 1, '_eAip'), ('eBi', 1, '_eBi'), ('eBip', 1, '_eBip'),

    ('Si', 1, '_Si'), ('Ci', 1, '_Ci'), ('Shi', 1, '_Shi'), ('Chi', 1, '_Chi'),
]


MPMATH_FUNCTION_NAMES: FunctionNames = [
    ('sec', 1, None), ('csc', 1, None), ('cot', 1, None),
    ('asec', 1, None), ('acsc', 1, None), ('acot', 1, None),
    ('cospi', 1, None), ('cospi', 1, None),
    ('sinc', 1, None),
    ('sech', 1, None), ('csch', 1, None), ('coth', 1, None),
    ('asech', 1, None), ('acsch', 1, None), ('acoth', 1, None),

    ('fac2', 1, None),
    ('rf', 1, None), ('ff', 1, None),
    ('superfac', 1, None), ('hyperfac', 1, None), ('barnesg', 1, None),
    ('harmonic', 1, None),

    ('Ei', 1, 'ei'), ('Li', 1, '_Li'), ('li', 1, None),

    ('angerj', 2, None), ('webere', 2, None),
    ('lommels1', 3, None), ('lommels2', 3, None),
    ('scorergi', 1, None), ('scorerhi', 1, None),
    ('coulombf', 3, None), ('coulombg', 3, None), ('coulombc', 2, None),
    ('whitm', 3, None), ('whitw', 3, None),
    ('pcfd', 2, None), ('pcfu', 2, None), ('pcfv', 2, None), ('pcfw', 2, None),

    ('legendre', 2, None), ('legenp', 3, None), ('legenq', 3, None),
    ('chebyt', 2, None), ('chebyu', 2, None),
    ('jacobi', 4, None), ('gegenbauer', 3, None), ('hermite', 2, None), ('laguerre', 3, None),

    ('hyp1f2', 4, None), ('hyp2f0', 3, None), ('hyp2f3', 5, None), ('hyp3f2', 6, None),

    ('ellipf', 2, None), ('ellippi', 3, None),

    ('altzeta', 1, None), ('stieltjes', 1, None), ('siegelz', 1, None), ('siegeltheta', 1, None),
    ('backlunds', 1, None), ('lerchphi', 3, None),
    ('polylog', 2, None), ('clsin', 2, None), ('clcos', 2, None), ('polyexp', 2, None),
    ('primezeta', 1, None), ('secondzeta', 1, None),

    ('fib', 1, None), ('fibonacci', 1, None),
    ('primepi', 1, None), ('riemannr', 1, None),

    ('betainc2', 4, 'betainc'),

    ('gammainc2', 3, 'gammainc'),

    ('eta', 1, 'altzeta'), ('nzetazeros', 1, 'nzeros')
]


PROBABILITY_FUNCTION_NAMES: FunctionNames = [
    ('normpdf', 3, 'norm_pdf'), ('normcdf', 3, 'norm_cdf'),
    ('unormpdf', 1, 'unit_norm_pdf'), ('unormcdf', 1, 'unit_norm_cdf'),

    ('tripdf', 4, 'triangle_pdf'), ('tricdf', 4, 'triangle_cdf'),

    ('uniformpdf', 3, 'uniform_pdf'), ('uniformcdf', 3, 'uniform_cdf'),

    ('exppdf', 2, 'expon_pdf'), ('expcdf', 2, 'expon_cdf'),

    ('studentpdf', 2, 'student_pdf'), ('studentcdf', 2, 'student_cdf'),

    ('betapdf', 3, 'beta_pdf'), ('betacdf', 3, 'beta_cdf'),

    ('chi2pdf', 2, 'chi2_pdf'), ('chi2cdf', 2, 'chi2_cdf'),
    ('khi2pdf', 2, 'chi2_pdf'), ('khi2cdf', 2, 'chi2_cdf'),

    ('gammapdf', 3, 'gamma_pdf'), ('gammacdf', 3, 'gamma_cdf'),

    ('cauchypdf', 3, 'cauchy_pdf'), ('cauchycdf', 3, 'cauchy_cdf'),
]


OTHER_FUNCTION_NAMES: FunctionNames = [
    ('relu', 1, None), ('lrelu', 2, 'leaky_relu'),

    ('sigmoid', 1, None), ('sigm', 1, 'sigmoid'), 

    ('sign', 1, None), ('sgn', 1, 'sign'),

    ('lerp', 5, None), ('lerpt', 3, None),

    ('heaviside', 1, None),
    ('ramp', 1, 'relu'),
    ('rect', 1, None),
    ('triangle', 1, None), ('tri', 1, 'triangle'),

    ('sawtooth', 1, None),
    ('squarewave', 1, None), ('sqwave', 1, 'squarewave'),
    ('trianglewave', 1, None), ('triwave', 1, 'trianglewave'),

    ('if', 3, '_if'), ('ifn', 3, None), ('ifz', 3, None),
    ('in', 5, '_in'), ('out', 5, None),
]
