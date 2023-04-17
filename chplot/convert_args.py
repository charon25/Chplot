import argparse
import logging
from typing import IO

logger = logging.getLogger(__name__)


def _get_non_empty_lines(fi: IO) -> list[str]:
    return (line.strip() for line in fi if line != '\n')


def retrieve_constants(parameters: argparse.Namespace) -> None:
    """Retrieve in-place all constants that are in files."""

    constants: list[str] = parameters.constants_arg
    if constants is None:
        parameters.constants = []
        return

    final_constants: list[str] = []
    for constant in constants:
        try:
            with open(constant, 'r', encoding='utf-8') as fi:
                final_constants.extend(_get_non_empty_lines(fi))

        # If the file is not found, it means it should be an expression
        except (FileNotFoundError, OSError):
            final_constants.append(constant)

        # For every other exception, log and ignore
        except Exception:
            logger.warning("error while opening file '%s', the file will be ignored.", constants)

    parameters.constants = final_constants


def retrieve_expressions(parameters: argparse.Namespace) -> None:
    """Retrieve in-place all expressions that are in files."""

    final_expressions: list[str] = []
    for expression in parameters.expressions:
        try:
            with open(expression, 'r', encoding='utf-8') as fi:
                final_expressions.extend(_get_non_empty_lines(fi))

        # If the file is not found, it means it should be an expression
        except (FileNotFoundError, OSError):
            final_expressions.append(expression)

        # For every other exception, log and ignore
        except Exception:
            logger.warning("error while opening file '%s', the file will be ignored.", expression)

    parameters.expressions = final_expressions
