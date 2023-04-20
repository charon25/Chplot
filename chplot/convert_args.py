import re
from typing import IO, Optional

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import LOGGER


CONSTANT_DEFAULT_REGRESSION_KEYWORDS: dict[str, str] = {
    'const': '_rm',
    'constant': '_rm',
    'lin': '_ra * x + _rb',
    'linear': '_ra * x + _rb',
    'power': '_rk * (x^_ralpha)',
    'powery': '_rk * (x^_ralpha) + _ry0',
    'log': '_ra * ln(x) + _rb',
    'exp': '_ra * exp(x * _rb)',
    'expy': '_ra * exp(x * _rb) + _ry0',
}


def _get_non_empty_lines(fi: IO) -> list[str]:
    return (line.strip() for line in fi if line != '\n')


def retrieve_constants(parameters: PlotParameters) -> None:
    """Retrieve in-place all constants that are in files."""

    constants: list[str] = parameters.constants_arg
    if constants is None:
        parameters.constants = []
        return

    final_constants: list[str] = []
    for constant in constants:
        try:
            with open(constant, 'r', encoding='utf-8') as file:
                final_constants.extend(_get_non_empty_lines(file))

        # If the file is not found, it means it should be an expression
        except (FileNotFoundError, OSError):
            final_constants.append(constant)

        # For every other exception, log and ignore
        except Exception:
            LOGGER.error("error while opening file '%s', the file will be ignored", constants)

    parameters.constants = final_constants


def retrieve_expressions(parameters: PlotParameters) -> None:
    """Retrieve in-place all expressions that are in files."""

    final_expressions: list[str] = []
    for expression in parameters.expressions:
        try:
            with open(expression, 'r', encoding='utf-8') as file:
                final_expressions.extend(_get_non_empty_lines(file))

        # If the file is not found, it means it should be an expression
        except (FileNotFoundError, OSError):
            final_expressions.append(expression)

        # For every other exception, log and ignore
        except Exception:
            LOGGER.error("error while opening file '%s', the file will be ignored", expression)

    parameters.expressions = final_expressions


def _get_monomial(degree: int) -> str:
    if degree == 0:
        return '_ra0'
    if degree == 1:
        return '_ra1 * x'
    return f'_ra{degree} * x^{degree}'


def get_default_regression_expression(regression_expression: Optional[str]) -> Optional[str]:
    """Return the correct expression of some default regression expression."""

    if regression_expression is None:
        return None

    if regression_expression in CONSTANT_DEFAULT_REGRESSION_KEYWORDS:
        return CONSTANT_DEFAULT_REGRESSION_KEYWORDS[regression_expression]

    # Matches pX, polyX or polynomialX where X is any non negative integer
    if (match := re.findall(r'^p(?:(?:oly)(?:nomial)?)?(\d+)$', regression_expression)):
        degree = int(match[0])
        return ' + '.join(map(_get_monomial, range(degree, -1, -1)))



    return regression_expression
