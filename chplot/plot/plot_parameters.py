from dataclasses import dataclass, fields
import math
from typing import Any, Literal, Optional, Union

from shunting_yard import shunting_yard

from chplot.rpn import compute_rpn_unsafe, get_rpn_errors


@dataclass
class PlotParameters:
    expressions: list[str]
    variable: Optional[str]

    n_points: Optional[int]
    is_integer: Optional[bool]

    x_lim: Optional[tuple[str, str]]
    is_x_log: Optional[bool]

    y_lim: Optional[tuple[str, str]]
    must_contain_zero: Optional[bool]
    is_y_log: Optional[bool]

    x_label: Optional[str]
    y_label: Optional[str]
    title: Optional[str]
    remove_legend: Optional[bool]
    plot_without_lines: Optional[bool]

    zeros_file: Optional[Union[Literal[0], str]]
    no_plot: Optional[bool]


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
)


def set_default_values(parameters: PlotParameters) -> None:
    """Add missing field and set default values if fields are set to None. In-place."""
    for field in fields(PlotParameters):
        field_name = field.name
        if not hasattr(parameters, field_name) or getattr(parameters, field_name) is None:
            setattr(parameters, field_name, getattr(DEFAULT_PARAMETERS, field_name))

def _convert_single_expression(expression: str, default_value: Any) -> float:
    rpn = shunting_yard(expression, case_sensitive=True, variable=None)

    if get_rpn_errors(rpn, variable=None) is not None:
        return default_value

    value = compute_rpn_unsafe(rpn.split(' '), 0, variable=None)
    return value if not math.isnan(value) else default_value


def convert_parameters_expression(parameters: PlotParameters) -> None:
    """Convert every mathematical expression in fields (except the 'expressions' field) to its float value. In-place."""
    parameters.x_lim = (
        _convert_single_expression(
            str(parameters.x_lim[0]), default_value=float(DEFAULT_PARAMETERS.x_lim[0])
        ),
        _convert_single_expression(
            str(parameters.x_lim[1]), default_value=float(DEFAULT_PARAMETERS.x_lim[1])
        ),
    )

    parameters.y_lim = (
        _convert_single_expression(
            str(parameters.y_lim[0]), default_value=DEFAULT_PARAMETERS.y_lim[0]
        ),
        _convert_single_expression(
            str(parameters.y_lim[1]), default_value=DEFAULT_PARAMETERS.y_lim[1]
        ),
    )
