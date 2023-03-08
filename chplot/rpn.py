import math
from typing import Iterator


from chplot.functions import FUNCTIONS #TODO changer l'origine pour ajouter constantes/fonctions custom


class NotEnoughParametersError(Exception):
    pass
class TooManyResultsError(Exception):
    pass
class UnknownFunction(Exception):
    pass


NUMBER_CHARS = '0123456789.'


def check_rpn_validity(rpn_tokens: list[str], variable: str = 'x') -> bool:
    """Check if the given RPN is a valid one. If yes, return True. If no, will raise an exception (UnknownFunction, NotEnoughParametersError or TooManyResultsError)."""
    stack: list[float] = []

    for token in rpn_tokens:
        if token[0] in NUMBER_CHARS:
            # Convert to float or int according to the presence of a dot
            stack.append(float(token) if '.' in token else int(token))
        elif token == variable:
            stack.append(0)
        else:
            if not token in FUNCTIONS:
                raise UnknownFunction(f'unknown function : {token}')

            param_count, func = FUNCTIONS[token]

            if param_count == 0:
                stack.append(func)
                continue

            if len(stack) < param_count:
                raise NotEnoughParametersError(f"not enough parameters for function '{token}' : {len(stack)} found, {param_count} expected.")
            parameters = stack[-param_count:]
            stack = stack[:-param_count]

            try:
                result = func(*parameters)
            except Exception:
                result = 0

            stack.append(result)

    if len(stack) > 1:
        raise TooManyResultsError(f"expression does not give only one result.")

    return True


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

            if param_count == 0:
                stack.append(func)
                continue

            parameters = stack[-param_count:]
            stack = stack[:-param_count]

            try:
                result = func(*parameters)
            except Exception:
                return math.nan

            stack.append(result)

    result = stack[0]
    if math.isinf(result):
        return math.nan

    return result


def compute_rpn_list(rpn: str, inputs: float, variable: str = 'x') -> Iterator[float]:
    rpn_tokens = rpn.split()

    for x in inputs:
        yield compute_rpn_unsafe(rpn_tokens, x, variable)


