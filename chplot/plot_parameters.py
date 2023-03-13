from dataclasses import dataclass
from typing import Optional


@dataclass
class PlotParameters:
    expressions: list[str]
    variable: Optional[str]

    n_points: Optional[int]
    is_integer: Optional[bool]

    x_lim: Optional[tuple[float, float]]
    is_x_log: Optional[bool]

    y_lim: Optional[tuple[float, float]]
    must_contain_zero: Optional[bool]
    is_y_log: Optional[bool]

    x_label: Optional[str]
    y_label: Optional[str]
    title: Optional[str]
    remove_legend: Optional[str]

    compute_zeros: Optional[bool]


DEFAULT_PARAMETERS = PlotParameters(
    expressions=[],
    variable='x',

    n_points=10000,
    is_integer=False,

    x_lim=(0.0, 1.0),
    is_x_log=False,

    y_lim=None,
    must_contain_zero=False,
    is_y_log=False,

    x_label=None,
    y_label=None,
    title=None,
    remove_legend=False,

    compute_zeros=False,
)
