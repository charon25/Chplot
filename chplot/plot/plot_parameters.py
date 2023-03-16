from dataclasses import dataclass, fields
import logging
import math
from typing import Any, Literal, Optional, Union

from shunting_yard import shunting_yard

from chplot.functions import FUNCTIONS
from chplot.functions.utils import FunctionDict
from chplot.rpn import compute_rpn_unsafe, get_rpn_errors


logger = logging.getLogger(__name__)


@dataclass
class PlotParameters:
    expressions: list[str]
    variable: Optional[str]

    n_points: Optional[int]
    is_integer: Optional[bool]

    x_lim: Optional[Union[tuple[str, str], tuple[float, float]]]
    is_x_log: Optional[bool]

    y_lim: Optional[Union[tuple[str, str], tuple[float, float]]]
    must_contain_zero: Optional[bool]
    is_y_log: Optional[bool]

    x_label: Optional[str]
    y_label: Optional[str]
    title: Optional[str]
    remove_legend: Optional[bool]
    plot_without_lines: Optional[bool]

    zeros_file: Optional[Union[Literal[0], str]]
    no_plot: Optional[bool]
    integral_file: Optional[Union[Literal[0], str]]

    constants: Optional[Union[list[str], FunctionDict]]


DEFAULT_PARAMETERS = PlotParameters(
    expressions=[],
    variable='x',

    n_points=10001,
    is_integer=False,

    x_lim=("0.0", "1.0"),
    is_x_log=False,

    y_lim=(None, None),
    must_contain_zero=False,
    is_y_log=False,

    x_label=None,
    y_label=None,
    title=None,
    remove_legend=False,
    plot_without_lines=False,

    zeros_file=None,
    no_plot=False,
    integral_file=None,

    constants=lambda:[], # prevents reference copying
)


def set_default_values(parameters: PlotParameters) -> None:
    """Add missing field and set default values if fields are set to None. In-place."""
    for field in fields(PlotParameters):
        field_name = field.name
        if not hasattr(parameters, field_name) or getattr(parameters, field_name) is None:
            default_attr = getattr(DEFAULT_PARAMETERS, field_name)
            if callable(default_attr):
                setattr(parameters, field_name, default_attr())
            else:
                setattr(parameters, field_name, default_attr)


def _convert_single_expression(expression: str, default_value_error: Any, default_value_nan: Any = None) -> float:
    if default_value_nan is None:
        default_value_nan = default_value_error

    rpn = shunting_yard(expression, case_sensitive=True, variable=None)

    if get_rpn_errors(rpn, variable=None) is not None:
        return default_value_error

    value = compute_rpn_unsafe(rpn.split(' '), 0, variable=None)
    return value if not math.isnan(value) else default_value_nan


def convert_parameters_expression(parameters: PlotParameters) -> None:
    """Convert every mathematical expression in fields (except the 'expressions' field) to its float value. In-place."""
    parameters.x_lim = (
        _convert_single_expression(
            str(parameters.x_lim[0]), default_value_error=float(DEFAULT_PARAMETERS.x_lim[0])
        ),
        _convert_single_expression(
            str(parameters.x_lim[1]), default_value_error=float(DEFAULT_PARAMETERS.x_lim[1])
        ),
    )

    parameters.y_lim = (
        _convert_single_expression(
            str(parameters.y_lim[0]), default_value_error=DEFAULT_PARAMETERS.y_lim[0]
        ),
        _convert_single_expression(
            str(parameters.y_lim[1]), default_value_error=DEFAULT_PARAMETERS.y_lim[1]
        ),
    )

    constants_function_dict: FunctionDict = {}
    for constant in parameters.constants:
        try:
            constant_name, constant_expression = constant.split('=')
            constant_name = constant_name.strip()
        except Exception:
            logger.warning("cannot parse constant assignement '%s', it will be ignored. If it is a file, this may error may be generated if errors occured during file opening.", constant)
            continue

        constant_value = _convert_single_expression(constant_expression, default_value_error=None, default_value_nan=math.nan)
        if constant_value is None:
            logger.warning("error while computing constant expression '%s' (of constant '%s'), it will be ignored.", constant_expression, constant_name)
            continue

        # 0 indicates it's a constant and do not require parameters
        if constant_name in FUNCTIONS:
            logger.warning("constant '%s' will replace an already defined constant/function.", constant_name)
        FUNCTIONS[constant_name] = (0, constant_value)
        # constants_function_dict[constant_name] = (0, constant_value)

    parameters.constants = constants_function_dict
