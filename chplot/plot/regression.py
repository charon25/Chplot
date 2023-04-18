import logging
import re
import sys
from typing import Optional, Union
import numpy as np

from scipy.optimize import curve_fit
from shunting_yard import MismatchedBracketsError, shunting_yard

from chplot.functions import FUNCTIONS
from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph, GraphType
from chplot.rpn import compute_rpn_list, get_rpn_errors


logger = logging.getLogger(__name__)

# match anything like _rX either at the beginning/end of a string or surrounded by spaces, where X is any string not containing spaces
REGRESSION_PARAMETERS_REGEX = r'(^| )(_r[^ ]+)( |$)'


def _check_regression_expression(parameters: PlotParameters) -> Optional[str]:
    """Check if the regression expression is valid. Return its RPN if yes, None if no."""

    try:
        rpn = shunting_yard(parameters.regression_expression, case_sensitive=True, variable=parameters.variable)
    except MismatchedBracketsError:
        logger.warning("mismatched brackets in the regression expression '%s'.", parameters.regression_expression)
        return None
    except Exception:
        logger.warning("unknown error in the regression expression '%s'.", parameters.regression_expression)
        return None

    # Check that there are regression parameters in the expression
    if not re.findall(REGRESSION_PARAMETERS_REGEX, rpn):
        logger.warning("error: no regression parameters (string starting with '_r' in the regression expression)")
        return None

    # Replace every regression parameters with 0 to check if the rest of the RPN is valid
    rpn_check = re.sub(REGRESSION_PARAMETERS_REGEX, r'\g<1>0\g<3>', rpn)
    if (error := get_rpn_errors(rpn_check, variable=parameters.variable)) is not None:
        logger.warning("error in the regression expression '%s' : %s", parameters.regression_expression, error)
        return None

    return rpn


def _get_fit_rpn(rpn: str, parameters_names: list[str], parameters_values: list[float]) -> str:
    """Return the given RPN with the regression parameters replaced by their values, so that the regression can be normally computed later."""

    for param_name, param_value in zip(parameters_names, parameters_values):
        rpn = re.sub(rf'(^| ){param_name}( |$)', rf'\g<1>{param_value}\g<2>', rpn)

    return rpn


def _get_fit_expression(expression: str, parameters_names: list[str], parameters_values: list[float]) -> str:
    """Return the given expression with the regression parameters replaced by their values. Brackets are added to force correct parsing by others softwares."""

    for param_name, param_value in zip(parameters_names, parameters_values):
        expression = re.sub(rf'\b{param_name}\b', f'({param_value})', expression)

    return expression


def _remove_nan(x: Union[list[float], np.ndarray], y: Union[list[float], np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Remove the values of both array where at least one of them is nan."""

    x = np.array(x)
    y = np.array(y)
    not_nan_indices = ~(np.isnan(x) | np.isnan(y))
    return (x[not_nan_indices], y[not_nan_indices])


# Ref : https://stackoverflow.com/questions/19189362/getting-the-r-squared-value-using-curve-fit
def _compute_r_squared(ydata: np.ndarray, yfit: np.ndarray):
    residuals = ydata - yfit
    sum_sq_res = np.sum(residuals ** 2)
    sum_sq_tot = np.sum((ydata - np.mean(ydata)) ** 2)

    print(sum_sq_res, sum_sq_tot)

    return 1 - sum_sq_res / sum_sq_tot


def compute_regressions(parameters: PlotParameters, graphs: list[Graph]) -> list[Graph]:
    if len(graphs) == 0:
        return []

    if (rpn := _check_regression_expression(parameters)) is None:
        return []

    file = sys.stdout

    # Get unique parameters without changing the order
    parameters_names = [param_name for _, param_name, _ in re.findall(REGRESSION_PARAMETERS_REGEX, rpn)]
    parameters_names = list(dict.fromkeys(parameters_names))


    def _regression_function(xdata: np.ndarray, *regression_parameters: list[float]):
        for (param_name, param_value) in zip(parameters_names, regression_parameters):
            FUNCTIONS[param_name] = (0, param_value)

        return compute_rpn_list(rpn, xdata, parameters.variable) #compute_rpn_unsafe(rpn_tokens, x, parameters.variable)

    regression_graphs: list[Graph] = []

    for graph in graphs:
        # Remove all nan values for the curve_fit computation
        inputs_without_nan, values_without_nan = _remove_nan(graph.inputs, graph.values)

        parameters_values, _ = curve_fit(
            f=_regression_function,
            xdata=inputs_without_nan,
            ydata=values_without_nan,
            p0=[1.0]*len(parameters_names)
        )

        custom_inputs = np.linspace(graph.inputs.min(), graph.inputs.max(), parameters.n_points, endpoint=True)

        r2 = _compute_r_squared(*_remove_nan(values_without_nan, _regression_function(inputs_without_nan, *parameters_values)))

        regression_graphs.append(Graph(
            inputs=custom_inputs,
            type=GraphType.REGRESSION,
            expression=f'Regression [{graph.expression}]',
            rpn=_get_fit_rpn(rpn, parameters_names, parameters_values),
            values=_regression_function(custom_inputs, *parameters_values)
        ))

        file.write(f'The coefficients of the regression of the {"data series" if graph.type == GraphType.FILE else "function f(x) = "} {graph.expression} are:\n')
        for param_name, param_value in zip(parameters_names, parameters_values):
            file.write(f'  {param_name[2:]} = {param_value}\n')
        file.write(f'On the interval [{graph.inputs.min():.3f} ; {graph.inputs.max():.3f}] R2 = {r2}\n')
        file.write(f'Copyable expression: f(x) = {_get_fit_expression(parameters.regression_expression, parameters_names, parameters_values)}\n\n')

    return regression_graphs

