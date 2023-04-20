from enum import Enum
import math
import ntpath
import re

import numpy as np

from chplot.plot.plot_parameters import PlotParameters
from chplot.plot.utils import Graph, GraphType
from chplot.plot.utils import LOGGER


NUMERIC_CHARS = '0123456789+-.,'
REGEX_COMMA_DECIMAL_SEP = r'^-?\d*(,?)\d*(?:e[+-]?\d+)?([;\t ])'
REGEX_DOT_DECIMAL_SEP = r'^-?\d*(\.?)\d*(?:e[+-]?\d+)?([,;\t ])'
# Match any odd number of quotes not at the beginning or the end of the string
REGEX_ILLEGAL_QUOTES = r'(?<!^)(?<!")"("")*(?!")(?!$)'
REGEX_START_WITH_QUOTES = r'^"("")*([^"]|$)'
REGEX_END_WITH_QUOTES = r'(^|[^"])"("")*$'
QUOTES = '"'
TWO_QUOTES = QUOTES * 2

class DecimalSeparator(Enum):
    DOT = 0
    COMMA = 1
    UNKNOWN = 2

class IllegalQuotesError(ValueError):
    pass


def _is_line_numeric(line: str) -> bool:
    return line != '' and line[0] in NUMERIC_CHARS


def _get_line_format(lines: list[str]) -> tuple[str, DecimalSeparator]:
    """Return the delimiter of the csv file."""

    for line in lines:
        line = line.strip()
        if not _is_line_numeric(line):
            continue

        if (result := re.findall(REGEX_COMMA_DECIMAL_SEP, line)):
            decimal_separator, column_separator = result[0]
            return (column_separator, DecimalSeparator.COMMA if decimal_separator == ',' else DecimalSeparator.UNKNOWN)

        if (result := re.findall(REGEX_DOT_DECIMAL_SEP, line)):
            decimal_separator, column_separator = result[0]

            if decimal_separator == '.' or (decimal_separator == '' and column_separator == ','):
                return (column_separator, DecimalSeparator.DOT)
            return (column_separator, DecimalSeparator.UNKNOWN)

    return ('', DecimalSeparator.UNKNOWN)


def _get_column_names(line: str, column_separator: str) -> list[str]:
    columns: list[str] = []
    current_column_start = 0
    in_quotes = False

    pseudo_columns = line.split(column_separator)

    # Split according to the separator, and then join pieces inside quotes
    for index, pseudo_column in enumerate(pseudo_columns):
        # If there are any quotes not doubled except for the start and end of the string
        # those are illegal quotes
        if re.search(REGEX_ILLEGAL_QUOTES, pseudo_column):
            raise IllegalQuotesError()

        if re.search(REGEX_START_WITH_QUOTES, pseudo_column):
            in_quotes = True
        if re.search(REGEX_END_WITH_QUOTES, pseudo_column):
            in_quotes = False

        if not in_quotes:
            column = column_separator.join(pseudo_columns[current_column_start:index+1])
            columns.append(column.strip(QUOTES).replace(TWO_QUOTES, QUOTES))
            current_column_start = index + 1

    return columns


def _to_float_or_nan(x: str) -> float:
    try:
        return float(x)
    except ValueError:
        return math.nan

def _get_filename(filepath: str) -> str:
    return ntpath.basename(filepath)

def _read_one_file(filepath: str) -> list[Graph]:
    # read all at once because we may need to backtrack to get the title line
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

    column_separator, decimal_separator = _get_line_format(lines)
    column_names: list[str] = []
    inputs_list: list[list[float]] = []
    values_list: list[list[float]] = []

    for line in lines:
        line = line.strip()
        if _is_line_numeric(line):
            if decimal_separator in (DecimalSeparator.COMMA, DecimalSeparator.UNKNOWN):
                line = line.replace(',', '.')

            x, *values = map(_to_float_or_nan, line.split(column_separator))
            # If there are no x value, just ignore the line
            if math.isnan(x):
                continue

            # If there are suddenly a new columns, increase the inputs and values count
            if len(values) > len(inputs_list):
                inputs_list.extend(([] for _ in  range(len(values) - len(inputs_list))))
                values_list.extend(([] for _ in  range(len(values) - len(values_list))))

            for index, value in enumerate(values):
                if not math.isnan(value):
                    inputs_list[index].append(x)
                    values_list[index].append(value)

        else:
            if line != '' and not column_names:
                column_names = [f'{_get_filename(filepath)} - {column_name}' for column_name in _get_column_names(line, column_separator)]

    # Remove the first column, as we do not care about the x label
    column_names = column_names[1:]
    if len(column_names) < len(values_list):
        # Extend will change column_names length between each iteration, so we need to store the offset before
        offset = len(column_names) + 1
        column_names.extend([
            f'{_get_filename(filepath)} - Column {index + offset}'
            for index in range(len(values_list) - len(column_names))
        ])


    return [
        Graph(np.array(inputs_list[index]), GraphType.FILE, column_names[index], None, values)
        for index, values in enumerate(values_list)
    ]



def read_files(parameters: PlotParameters) -> list[Graph]:
    graphs: list[Graph] = []
    for filepath in parameters.data_files:
        try:
            graphs.extend(_read_one_file(filepath))
        except FileNotFoundError:
            LOGGER.error("file '%s' does not exist or is unreachable", filepath)
        except OSError:
            LOGGER.error("error while opening file '%s'", filepath)
        except Exception:
            LOGGER.error("unknown error while reading file '%s'", filepath)

    return graphs
