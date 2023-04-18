import re
import sys
from typing import Optional, Union

import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
from shunting_yard import MismatchedBracketsError, shunting_yard
from tqdm import tqdm

from chplot.functions import FUNCTIONS
from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import _round as round
from chplot.plot.utils import Graph, GraphType
from chplot.plot.utils import LOGGER
from chplot.rpn import compute_rpn_list, get_rpn_errors


# match anything like _rX either at the beginning/end of a string or surrounded by spaces, where X is a letter or underscore possibly followed by more letters/underscores or digits
REGRESSION_PARAMETERS_REGEX = r'(^| )(_r[a-zA-Z_][0-9a-zA-Z_]*)( |$)'


def _get_unique_regression_parameters(rpn: str) -> list[str]:
    """Get unique regression parameters without changing their order, and without missing overlapping parameters."""

    parameters_names = []#[param_name for _, param_name, _ in re.findall(REGRESSION_PARAMETERS_REGEX, rpn)]
    while rpn:
        match = re.search(REGRESSION_PARAMETERS_REGEX, rpn)
        if match:
            rpn = rpn[match.start() + 1:]
            if (param_name := match.group(2)) not in parameters_names:
                parameters_names.append(param_name)
        else:
            break

    return parameters_names



def _check_regression_expression(parameters: PlotParameters) -> Optional[str]:
    """Check if the regression expression is valid. Return its RPN if yes, None if no."""

    try:
        rpn = shunting_yard(parameters.regression_expression, case_sensitive=True, variable=parameters.variable)
    except MismatchedBracketsError:
        LOGGER.error("mismatched brackets in the regression expression '%s'.", parameters.regression_expression)
        return None
    except Exception:
        LOGGER.error("unknown error in the regression expression '%s'.", parameters.regression_expression)
        return None

    # Check that there are regression parameters in the expression
    if not re.findall(REGRESSION_PARAMETERS_REGEX, rpn):
        LOGGER.error("error: no regression parameters (string starting with '_r' in the regression expression)")
        return None

    # Replace every regression parameters with 0 to check if the rest of the RPN is valid
    # If parameters are overlapping (ie: the rpn contains something like "_ra _rb"), we need to do the replacement multiple times
    rpn_check = rpn
    while re.search(REGRESSION_PARAMETERS_REGEX, rpn_check):
        rpn_check = re.sub(REGRESSION_PARAMETERS_REGEX, r'\g<1>0\g<3>', rpn_check)

    if (error := get_rpn_errors(rpn_check, variable=parameters.variable)) is not None:
        LOGGER.error("error in the regression expression '%s' : %s", parameters.regression_expression, error)
        return None

    return rpn


def _get_fit_rpn(rpn: str, parameters_names: list[str], parameters_values: list[float]) -> str:
    """Return the given RPN with the regression parameters replaced by their values, so that the regression can be normally computed later."""

    for param_name, param_value in zip(parameters_names, parameters_values):
        # abs function necessary to take care of -0.0
        if param_value >= 0:
            param_value_str = rf'\g<1>{abs(param_value)}\g<2>'
        # if the value is negative, we need to add a unary subtraction in the rpn
        else:
            param_value_str = rf'\g<1>{abs(param_value)} -u\g<2>'
        rpn = re.sub(rf'(^| ){param_name}( |$)', param_value_str, rpn)

    return rpn


def _get_fit_expression(expression: str, parameters_names: list[str], parameters_values: list[float], brackets: bool = True) -> str:
    """Return the given expression with the regression parameters replaced by their values. Brackets are added to force correct parsing by others softwares."""

    for param_name, param_value in zip(parameters_names, parameters_values):
        param_value_str = f'({param_value})' if brackets else str(param_value)
        expression = re.sub(rf'\b{param_name}\b', param_value_str, expression)

    return expression


def _remove_nan(arr1: Union[list[float], np.ndarray], arr2: Union[list[float], np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Remove the values of both arrays where at least one of them is nan."""

    arr1 = np.array(arr1)
    arr2 = np.array(arr2)
    not_nan_indices = ~(np.isnan(arr1) | np.isnan(arr2))
    return (arr1[not_nan_indices], arr2[not_nan_indices])


# Ref : https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
def _compute_r_squared_and_error(ydata: np.ndarray, yfit: np.ndarray) -> tuple[float, float]:
    residuals = ydata - yfit
    sum_sq_res = np.sum(residuals ** 2)
    sum_sq_tot = np.sum((ydata - np.mean(ydata)) ** 2)

    max_error = np.max(np.abs(residuals))

    if sum_sq_tot == 0:
        return (1, max_error)

    return (1 - sum_sq_res / sum_sq_tot, max_error)


def compute_regressions(parameters: PlotParameters, graphs: list[Graph]) -> list[Graph]:
    if len(graphs) == 0:
        return []

    if (rpn := _check_regression_expression(parameters)) is None:
        return []

    file = sys.stdout

    parameters_names = _get_unique_regression_parameters(rpn)
    parameters_names_without_prefix = [param_name[2:] for param_name in parameters_names]


    def _regression_function(xdata: np.ndarray, *regression_parameters: list[float]):
        for (param_name, param_value) in zip(parameters_names, regression_parameters):
            FUNCTIONS[param_name] = (0, param_value)

        pbar.update(1)

        return compute_rpn_list(rpn, xdata, parameters.variable, progress_bar=False)

    regression_graphs: list[Graph] = []

    file.write('\n===== REGRESSION COEFFICIENTS OF THE FUNCTIONS =====\n\n')

    file.write(f'Regression function: reg(x) = {_get_fit_expression(parameters.regression_expression, parameters_names, parameters_names_without_prefix, brackets=False)}\n\n')

    for graph in graphs:
        # Remove all nan values for the curve_fit computation
        inputs_without_nan, values_without_nan = _remove_nan(graph.inputs, graph.values)

        if inputs_without_nan.size < len(parameters_names):
            LOGGER.error(
                "not enough non-nan input points on graph '%s' to compute specified regression ('%s' found, at least '%s' needed)",
                graph.expression, inputs_without_nan.size, len(parameters_names)
            )
            continue

        try:
            # Default max number of iterations of curve_fit
            pbar = tqdm(total=200 * (len(parameters_names) + 1), leave=False)
            parameters_values, _ = curve_fit(
                f=_regression_function,
                xdata=inputs_without_nan,
                ydata=values_without_nan,
                p0=[1.0]*len(parameters_names)
            )
        except (OptimizeWarning, RuntimeError):
            pbar.close()
            LOGGER.error("error while computing regression of '%s', try reducing the number of parameters or simplifying the expression", graph.expression)
            continue

        pbar.close()

        custom_inputs = np.linspace(graph.inputs.min(), graph.inputs.max(), parameters.n_points, endpoint=True)

        r2, max_error = _compute_r_squared_and_error(*_remove_nan(values_without_nan, _regression_function(inputs_without_nan, *parameters_values)))

        regression_graphs.append(Graph(
            inputs=custom_inputs,
            type=GraphType.REGRESSION,
            expression=f'Regression [{graph.expression}]',
            rpn=_get_fit_rpn(rpn, parameters_names, parameters_values),
            values=_regression_function(custom_inputs, *parameters_values)
        ))


        file.write(f'- Function f(x) = {graph.expression}\n')
        file.write('  Coefficients:\n')
        for param_name, param_value in zip(parameters_names, parameters_values):
            file.write(f'    {param_name[2:]} = {round(param_value, 5)} (exact {param_value})\n')

        file.write(f'\n  Accuracy on [{graph.inputs.min():.3f} ; {graph.inputs.max():.3f}]:\n')
        file.write(f'    R2 = {r2}\n')
        file.write(f'    |err| <= {max_error}\n')
        file.write(f'\n  Copyable expression:\n    f(x) = {_get_fit_expression(parameters.regression_expression, parameters_names, parameters_values)}\n\n\n')

    return regression_graphs
