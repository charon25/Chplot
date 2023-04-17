import logging
import re
import sys
from typing import Optional
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

    # Replace every regression parameters with 0 to check if the rest of the RPN is valid
    rpn_check = re.sub(REGRESSION_PARAMETERS_REGEX, r'\g<1>0\g<3>', rpn)
    if (error := get_rpn_errors(rpn_check, variable=parameters.variable)) is not None:
        logger.warning("error in the regression expression '%s' : %s", parameters.regression_expression, error)
        return None
    
    return rpn


def _get_fit_rpn(rpn: str, parameters_names: list[str], parameters_values: list[float]) -> str:
    for param_name, param_value in zip(parameters_names, parameters_values):
        rpn = re.sub(rf'(^| ){param_name}( |$)', str(param_value), rpn)
    
    return rpn


def _get_fit_expression(expression: str, parameters_names: list[str], parameters_values: list[float]) -> str:
    for param_name, param_value in zip(parameters_names, parameters_values):
        expression = re.sub(rf'\b{param_name}\b', f'({param_value})', expression)
    
    return expression


def compute_regressions(parameters: PlotParameters, graphs: list[Graph]) -> list[Graph]:
    if (rpn := _check_regression_expression(parameters)) is None:
        return []

    file = sys.stdout
    
    # Get unique parameters without changing the order
    parameters_names = [param_name for _, param_name, _ in re.findall(REGRESSION_PARAMETERS_REGEX, rpn)]
    parameters_names = list(dict.fromkeys(parameters_names))
    if len(parameters_names) == 0:
        logger.warning("error: no regression parameters (string starting with '_r' in the regression expression)")
        return []
    
    def _regression_function(xdata: np.ndarray, *regression_parameters: list[float]):
        for (param_name, param_value) in zip(parameters_names, regression_parameters):
            FUNCTIONS[param_name] = (0, param_value)
        
        return compute_rpn_list(rpn, xdata, parameters.variable) #compute_rpn_unsafe(rpn_tokens, x, parameters.variable)

    regression_data: list[Graph] = []

    for graph in graphs:
        # if graph.type != GraphType.FILE:
        #     continue

        parameters_values, _ = curve_fit(
            f=_regression_function,
            xdata=graph.inputs,
            ydata=graph.values,
            p0=[1.0]*len(parameters_names)
        )

        custom_inputs = np.linspace(graph.inputs.min(), graph.inputs.max(), parameters.n_points, endpoint=True)

        regression_data.append(Graph(
            inputs=custom_inputs,
            type=GraphType.REGRESSION,
            expression=f'Regression [{graph.expression}]',
            rpn=_get_fit_rpn(rpn, parameters_names, parameters_values),
            values=_regression_function(custom_inputs, *parameters_values)
        ))

        file.write(f'The coefficients of the regression of the data series {graph.expression} are:\n')
        for param_name, param_value in zip(parameters_names, parameters_values):
            file.write(f'  {param_name[2:]} = {param_value}\n')
        file.write(f'Copyable expression: f(x) = {_get_fit_expression(parameters.regression_expression, parameters_names, parameters_values)}\n\n')




    return regression_data
