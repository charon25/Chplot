import math
from typing import Optional

import numpy as np
from tqdm import tqdm

from chplot.functions import FUNCTIONS


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
        return "expression does not give only one result."

    return None


def compute_rpn_unsafe(rpn_tokens: list[str], x: float, variable: str = 'x') -> float:
    """Compute the value of a RPN expression where every occurence of variable (default 'x') is replaced by the given value.
    Will return math.nan if either a function raises an exception (e.g. division by zero) or if the result is infinite (e.g. zeta(1)).
    This function can crash as it will not check for problems. Use get_rpn_errors first to know if the RPN is valid."""
    stack: list[float] = []

    for token in rpn_tokens:
        if type(token) in (int, float):
            stack.append(token)
        elif token[0] in NUMBER_CHARS:
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

    # Convert inf to nan so that max and min do not return inf or -inf
    return stack[0] if not math.isinf(stack[0]) else math.nan


def pre_compute_rpn(rpn_tokens: list[str], variable: str = 'x') -> list[str]:
    """Takes in RPN tokens and return RPN tokens with constant part computed.
    Does not check if the RPN is valid first, use get_rpn_errors to do it first."""

    if len(rpn_tokens) == 1:
        return rpn_tokens

    new_tokens: list[str] = []

    # Each time it encouters a function, try to apply it to the previous tokens
    # If it works, it was a constant, and the previous tokens are removed in favor of the result
    for token in rpn_tokens:
        if token[0] in NUMBER_CHARS or token == variable:
            new_tokens.append(token)
            continue

        param_count, func = FUNCTIONS[token]
        if param_count == 0:
            new_tokens.append(float(func))
            continue

        parameters = new_tokens[-param_count:]
        try:
            result = float(func(*map(float, parameters)))
            new_tokens = new_tokens[:-param_count]
            new_tokens.append(result)
        except Exception:
            new_tokens.append(token)

    return new_tokens


def compute_rpn_list(rpn: str, inputs: np.ndarray, variable: str = 'x', progress_bar: bool = True) -> list[float]:
    rpn_tokens = pre_compute_rpn(rpn.split(), variable=variable)

    if progress_bar:
        inputs_iter = tqdm(inputs, total=len(inputs), leave=False)
    else:
        inputs_iter = iter(inputs)

    return [compute_rpn_unsafe(rpn_tokens, float(x), variable) for x in inputs_iter]
