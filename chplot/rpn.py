import math
from typing import Iterator


from chplot.functions import FUNCTIONS


class WrongExpressionError(Exception):
    pass
class UnknownFunction(Exception):
    pass


NUMBER_CHARS = '0123456789.'

def compute_rpn_unsafe(rpn_tokens: list[str], x: float, variable: str = 'x') -> float:
    """Compute the value of a RPN expression where every occurence of variable (default 'x') is replaced by the given value.
    This function can crash as it will not check for problems. Use compute_rpn_safe for this case."""
    stack: list[float] = []

    for token in rpn_tokens:
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        elif token == variable:
            stack.append(x)
        else:
            param_count, func = FUNCTIONS[token]

            # Seperate both cases because l[-0:] is all the list and not an empty one
            if param_count > 0:
                parameters = stack[-param_count:]
                stack = stack[:-param_count]
            else:
                parameters = []

            try:
                result = func(*parameters)
            except Exception:
                return math.nan

            stack.append(result)

    return stack[0]

def compute_rpn_safe(rpn_tokens: list[str], x: float, variable: str = 'x') -> float:
    """Compute the value of a RPN expression where every occurence of variable (default 'x') is replaced by the given value."""
    stack: list[float] = []

    for token in rpn_tokens:
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        elif token == variable:
            stack.append(x)
        else:
            if not token in FUNCTIONS:
                raise UnknownFunction(f'unknown function : {token}')

            param_count, func = FUNCTIONS[token]

            # Seperate both cases because l[-0:] is all the list and not an empty one
            if param_count > 0:
                if len(stack) < param_count:
                    raise WrongExpressionError(f"not enough parameters for function '{token}' : {len(stack)} found, {param_count} expected.")
                parameters = stack[-param_count:]
                stack = stack[:-param_count]
            else:
                parameters = []

            try:
                result = func(*parameters)
            except Exception:
                return math.nan

            stack.append(result)

    if len(stack) > 1:
        raise WrongExpressionError(f"expression does not give only one result.")

    return stack[0]


def compute_rpn_list(rpn: str, inputs: float, variable: str = 'x') -> Iterator[float]:
    rpn_tokens = rpn.split()

    for x in inputs:
        yield compute_rpn_unsafe(rpn_tokens, x, variable)


