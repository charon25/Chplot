import argparse
import logging

logger = logging.getLogger(__name__)


def retrieve_constants(parameters: argparse.Namespace) -> None:
    """Retrieve all constants that are in files."""

    constants: list[str] = parameters.constants_arg
    if constants is None:
        parameters.constants = []
        return

    final_constants: list[str] = []
    for constant in constants:
        try:
            with open(constant, 'r', encoding='utf-8') as fi:
                final_constants.extend([line.strip() for line in fi if line != '\n'])

        # If the file is not found, it means it should be an expression
        except (FileNotFoundError, OSError):
            final_constants.append(constant)

        # For every other exception, log and ignore
        except Exception:
            logger.warning("error while opening file '%s', it will be ignored.", constants)

    parameters.constants = final_constants
