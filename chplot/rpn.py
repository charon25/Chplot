import logging
logger = logging.getLogger(__name__)
import math
from typing import Optional

from tqdm import tqdm


from chplot.functions import FUNCTIONS #TODO changer l'origine pour ajouter constantes/fonctions custom


NUMBER_CHARS = '0123456789.'


def get_rpn_errors(rpn: str, variable: str = 'x') -> Optional[str]:
    """Check if the given RPN is a valid one.
    Return either None if the RPN is valid, or the error message as a string if it is not."""
    stack: list[float] = []

    for token in rpn.split(' '):
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        elif token == variable:
            stack.append(0)
        else:
            if not token in FUNCTIONS:
                return f"unknown function: '{token}'"

            param_count, func = FUNCTIONS[token]

            if param_count == 0:
                stack.append(func)
                continue

            if len(stack) < param_count:
                return f"not enough parameters for function '{token}': {len(stack)} found, {param_count} expected."

            parameters = stack[-param_count:]
            stack = stack[:-param_count]

            try:
                result = float(func(*parameters))
            except Exception:
                result = 0

            stack.append(result)

    if len(stack) > 1:
        return f"expression does not give only one result."

    return None


def compute_rpn_unsafe(rpn_tokens: list[str], x: float, variable: str = 'x') -> float:
    """Compute the value of a RPN expression where every occurence of variable (default 'x') is replaced by the given value.
    Will return math.nan if either a function raises an exception (e.g. division by zero) or if the result is infinite (e.g. zeta(1)).
    This function can crash as it will not check for problems. Use get_rpn_errors first to know if the RPN is valid."""
    stack: list[float] = []

    for token in rpn_tokens:
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        elif token == variable:
            stack.append(x)
        else:
            param_count, func = FUNCTIONS[token]

            if param_count == 0:
                stack.append(func)
                continue

            parameters = stack[-param_count:]
            stack = stack[:-param_count]

            try:
                # Converts the result of the function/operation to a float
                # It's faster to try to convert and raise an Exception that to check the type
                # if we have a lot more right cases than wrong cases
                stack.append(float(func(*parameters)))
            except Exception:
                return math.nan

    # Convert inf to nan so that max and min does not return inf or -inf
    return stack[0] if not math.isinf(stack[0]) else math.nan


def compute_rpn_list(rpn: str, inputs: float, variable: str = 'x') -> list[float]:
    rpn_tokens = rpn.split()
    return [compute_rpn_unsafe(rpn_tokens, float(x), variable) for x in tqdm(inputs, total=len(inputs), leave=False)]
