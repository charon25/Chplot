from dataclasses import dataclass, field, fields
import importlib
import inspect
import math
import pathlib
import re
from types import BuiltinFunctionType, ModuleType
from typing import Any, Callable, Literal, Optional, Union

from shunting_yard import shunting_yard

from chplot.functions import FUNCTIONS
from chplot.functions.utils import FunctionDict
from chplot.plot.utils import DECORATOR_GETTER_REGEX, FUNCTION_NAME_REGEX, plottable
from chplot.plot.utils import LOGGER
from chplot.rpn import compute_rpn_unsafe, get_rpn_errors


@dataclass
class PlotParameters:
    expressions: list[str] = field(default_factory=lambda: [])
    variable: Optional[str] = 'x'

    n_points: Optional[int] = 10001
    is_integer: Optional[bool] = False

    x_lim: Optional[Union[tuple[str, str], tuple[float, float], tuple[None, None]]] = (None, None)
    is_x_log: Optional[bool] = False

    y_lim: Optional[Union[tuple[str, str], tuple[float, float], tuple[None, None]]]  = (None, None)
    must_contain_zero: Optional[bool] = False
    is_y_log: Optional[bool] = False

    x_label: Optional[str] = None
    y_label: Optional[str] = None
    title: Optional[str] = None
    remove_legend: Optional[bool] = False
    no_plot: Optional[bool] = False
    markersize: Optional[int] = None

    zeros_file: Optional[Union[Literal[0], str]] = None
    integral_file: Optional[Union[Literal[0], str]] = None
    derivation_orders: Optional[list[int]] = None
    regression_expression: Optional[str] = None

    constants: Optional[Union[list[str], FunctionDict]] = field(default_factory=lambda: [])
    data_files: Optional[list[str]] = None
    save_figure_path: Optional[str] = None
    save_data_path: Optional[str] = None
    python_files: Optional[str] = None


DEFAULT_PARAMETERS = PlotParameters()


def set_default_values(parameters: PlotParameters) -> None:
    """Add missing field and set default values in-place if fields are set to None. In-place."""
    for field in fields(PlotParameters):
        field_name = field.name
        if not hasattr(parameters, field_name) or getattr(parameters, field_name) is None:
            default_attr = getattr(DEFAULT_PARAMETERS, field_name)
            setattr(parameters, field_name, default_attr)


def _convert_single_expression(expression: Optional[str], default_value_nan: Any = None) -> float:
    if expression is None:
        return None

    if default_value_nan is None:
        default_value_nan = None

    rpn = shunting_yard(str(expression), case_sensitive=True, variable=None)

    if (error := get_rpn_errors(rpn, variable=None)) is not None:
        LOGGER.warning("error while computing expression '%s': %s", expression, error)
        return None

    value = compute_rpn_unsafe(rpn.split(' '), 0, variable=None)
    return value if not math.isnan(value) else default_value_nan


def convert_parameters_expression(parameters: PlotParameters) -> None:
    """Convert in-place every mathematical expression in fields (except the 'expressions' field) to its float value. In-place."""

    # Starts by the constant so they can be used by the x and y limits
    constants_function_dict: FunctionDict = {}
    for constant in parameters.constants:
        try:
            constant_name, constant_expression = constant.split('=')
            constant_name = constant_name.strip()
        except Exception:
            LOGGER.error("cannot parse constant assignement '%s', it will be ignored", constant)
            continue

        constant_value = _convert_single_expression(constant_expression, default_value_nan=math.nan)
        if constant_value is None:
            LOGGER.error("error while computing constant expression '%s' (of constant '%s'), it will be ignored", constant_expression, constant_name)
            continue

        # 0 indicates it's a constant and do not require parameters
        if constant_name in FUNCTIONS:
            LOGGER.warning("constant '%s' will replace an already defined constant or function", constant_name)
        FUNCTIONS[constant_name] = (0, constant_value)

    parameters.constants = constants_function_dict


    x_min, x_max = parameters.x_lim

    if x_min is not None:
        x_min = _convert_single_expression(x_min)
        if x_min is None:
            LOGGER.warning("cannot compute lower bound of x-axis")

    if x_max is not None:
        x_max = _convert_single_expression(x_max)
        if x_max is None:
            LOGGER.warning("cannot compute upper bound of x-axis")

    parameters.x_lim = (x_min, x_max)


    y_min, y_max = parameters.y_lim

    if y_min is not None:
        y_min = _convert_single_expression(y_min)
        if y_min is None:
            LOGGER.warning("cannot compute lower bound of y-axis")

    if y_max is not None:
        y_max = _convert_single_expression(y_max)
        if y_max is None:
            LOGGER.warning("cannot compute upper bound of y-axis")

    parameters.y_lim = (y_min, y_max)



def _get_decorated_functions(python: ModuleType) -> list[tuple[int, str, Callable]]:
    funcs: list[tuple[int, str, Callable]] = []
    for func in dir(python):
        func = getattr(python, func)
        if not callable(func) or func.__name__ == plottable.__name__:
            continue

        try:
            # do not care about built-ins
            if isinstance(func, BuiltinFunctionType):
                continue

            source_code = inspect.getsource(func)

            # This happens only if the decorator is without bracket
            if 'def decorator_plottable(func: Callable) -> Callable:' in source_code:
                LOGGER.error(
                    "the @plottable decorator is missing brackets on function '%s' of python file '%s.py', its source code is therefore inaccessible",
                    func.__name__,
                    python.__name__
                )

        except (OSError, TypeError):
            LOGGER.error("error while getting source code of function '%s' of python file '%s.py'", func.__name__, python.__name__)
            continue

        if (match := re.findall(DECORATOR_GETTER_REGEX, source_code)):
            arg_count = int(match[0]) if match[0] else 1
            funcs.append((arg_count, re.findall(FUNCTION_NAME_REGEX, source_code)[0], func))

    return funcs


def retrieve_python_functions(parameters: PlotParameters):
    """Retrieve in-place the decorated functions from the given python file."""

    if parameters.python_files is None:
        return

    for python_file in parameters.python_files:
        # try:
            # The file must be in the current directory
            if pathlib.Path(python_file).parent.parts:
                LOGGER.error("python file must be in the current directory ('%s')", python_file)
                continue

            # Remove the .py extension
            python_file = re.sub(r'\.py.*?$', '', python_file)
            python = importlib.import_module(python_file)
            for arg_count, func_name, func in _get_decorated_functions(python):
                try:
                    if func_name in FUNCTIONS:
                        LOGGER.warning("function or constant '%s' will replace an already defined constant or function", func_name)
                    # If the function is a constant (= does not have any argument), call it directly to optimize future computations
                    if arg_count == 0:
                        FUNCTIONS[func_name] = (0, func())
                    else:
                        FUNCTIONS[func_name] = (arg_count, func)
                except TypeError:
                    LOGGER.error("constant function '%s' of python file '%s' expected some arguments.", func_name, python_file)

        # except (ImportError, ModuleNotFoundError):
        #     LOGGER.error("error while importing python file '%s'.", python_file)
        # except Exception:
        #     LOGGER.error("unknown error while importing python file '%s'.", python_file)
