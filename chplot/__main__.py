import argparse
from chplot.convert_args import get_default_regression_expression, retrieve_constants, retrieve_expressions

from chplot.plot import plot


def positive_integer(value):
    try:
        value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: '{value}'")

    if value <= 0:
        raise argparse.ArgumentTypeError(f"invalid strictly positive integer: '{value}'")

    return value

def positive_float(value):
    try:
        value = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid int value: '{value}'")

    if value <= 0:
        raise argparse.ArgumentTypeError(f"invalid strictly positive integer: '{value}'")

    return value


def read_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chplot is a Python >= 3.9 module to plot any arbitrary mathematical expressions as well as data series from files, and compute its derivatives and integrals, where it equals zero, linear and non-linear regressions, and much more !\n\nDocumentation: https://github.com/charon25/Chplot")
    parser.add_argument('expressions', metavar='EXPRESSIONS', nargs='*', help='The expressions of the mathematical functions to plot and do computations on. Can also be filepaths containing expressions, one by line (except for line starting with #).')
    parser.add_argument('-v', '--variable', metavar='VARIABLE', dest='variable', help="The variable going of the horizontal axis. Can be more than one character. Note that the variable will override any constant of function with the same name. Defaults to 'x'.")
    parser.add_argument('--no-sn', action='store_true', dest='disable_scientific_notation', help="Disable the automatic conversion of scientific notation in every expression (e.g. '1.24e-1' to '1.24*10^(-1)').")

    parser.add_argument('-n', '--n-points', metavar='POINTS', type=positive_integer, dest='n_points', help='The number of points on the horizontal axis for the plotting of the expressions. Defaults to 10001.')
    parser.add_argument('-i', '--integers', action='store_true', dest='is_integer', help='Forces the points where the expressions are computed to be integers between the specified limits. The number of points will not exceed what is specified with the `-n` parameter. Defaults to False.')

    parser.add_argument('-x', '--x-lim', nargs=2, metavar=('X_MIN', 'X_MAX'), dest='x_lim', help="The horizontal axis bounds (inclusive) where the expression are computed. First argument is the min, second is the max. Any expression (such as '2pi' or '1+exp(2)') is valid. It is also the graph default horizontal axis, but they can be automatically adjusted to accomodate the plotted data. Defaults to 0 1.")
    parser.add_argument('-xlog', '-xlog', action='store_true', dest='is_x_log', help="	Forces a logarithmic scale on the horizontal axis. If some horizontal axis bounds are negative, will modify them. Defaults to False.")

    parser.add_argument('-y', '--y-lim', nargs=2, metavar=('Y_MIN', 'Y_MAX'), dest='y_lim', help="The vertical axis bounds (inclusive) of the graph. First argument is the min, second is the max. Any expression (such as '2pi' or '1+exp(2)') is valid. If not specified, will use matplotlib default ones to accomodate all data. Will restrict the graph to them is specified.")
    parser.add_argument('-z', '--y-zero', action='store_true', dest='must_contain_zero', help='Forces the vertical axis to contain zero. Defaults to False.')
    parser.add_argument('-ylog', '--ylog', action='store_true', dest='is_y_log', help="Forces a logarithmic scale on the vertical axis. If some vertical axis bounds are negative, will modify them. Defaults to False.")

    parser.add_argument('-xl', '--x-label', metavar='X_LABEL', dest='x_label', help='Label of the horizontal axis. Defaults to nothing.')
    parser.add_argument('-yl', '--y-label', metavar='Y_LABEL', dest='y_label', help='Label of the vertical axis. Defaults to nothing.')
    parser.add_argument('-t', '--title', metavar='TITLE', dest='title', help='Title of the graph. Defaults to nothing.')
    parser.add_argument('-rl', '--remove-legend', action='store_true', dest='remove_legend', help='Removes the graph legend.')
    parser.add_argument('--no-plot', action='store_true', dest='no_plot', help='Does not show the plot. However, does not prevent saving the figure.')
    parser.add_argument('-dis', '--discontinuous', nargs='?', const=1, type=positive_integer, dest='markersize', help='Transforms the style of the graph from a continuous line to discrete points with the specified radius. If present without a value, will defaults to a radius of 1. If the --integer parameter is also present, will still affect the points radius.')
    parser.add_argument('--square', action='store_true', dest='square_graph', help="Forces the graph to be a square (aspect ratio of 1).")
    parser.add_argument('-lw', '--line-width', default=1, type=positive_float, dest='line_width', help='Width of the plotted functions. Will not affect regressions. Defaults to 1.5 (matplotlib defaut).')

    parser.add_argument('--zeros', nargs='?', const=0, dest='zeros_file', help='Computes where the expressions equal zero. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file.')
    parser.add_argument('-int', '--integral', nargs='?', const=0, dest='integral_file', help='Computes the integral of all functions on the entire interval where it is plotted. Note that it does not add the antideritive of the functions to the graph, but only computes the area under them on their definition interval. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file.')
    parser.add_argument('-deriv', '--derivatives', nargs='+', dest='derivation_orders', type=positive_integer, help='Computes and adds to the graph the derivative of the specified orders of every other function. Note that the higher the order, the more inaccuracy and unstability it has. Furthermore, the derivative computation will shave off a few points on each side, so the derivatives are defined on a smaller interval.')
    parser.add_argument('-reg', '--regression', dest='regression_expression', metavar='REGRESSION_EXPRESSION', help="Computes the coefficients of the given regression to get the best fit to every other function. The regression parameters should have the form _rX where X is any string made of digits, letters and underscores and starting with a letter (eg '_ra0'). The regressions will also be added in the final graph. It can also be one of a few default keywords (listed in the Regression default keywords section of the documentation).")

    parser.add_argument('-c', '--constants', nargs='+', dest='constants_arg', metavar=('CONSTANT', 'CONSTANT'), help="Adds constants which may be used by any other expressions (including axis bounds). They must either be of the form '<name>=<expression>' (eg 'a=4sin(pi/4))') or be filepath containing lines respecting this format. May override already existing constants and functions. If a constant refers to another one, it should be defined after. Defaults to nothing.")
    parser.add_argument('-f', '--files', nargs='+', dest='data_files', metavar=('CSV_FILE', 'CSV_FILE'), help='Adds data contained in CSV files as new functions to the graph. See the CSV files format section of the documentation for more details.')
    parser.add_argument('-s', '--save-graph', dest='save_figure_path', metavar='FIGURE_FILE', help='Saves the graph at the specified path.')
    parser.add_argument('-d', '--save-data', dest='save_data_path', metavar='DATA_FILE', help='Saves the graph data (x and y values) at the specified path in CSV format.')
    parser.add_argument('-p', '--python-files', nargs='+', dest='python_files', metavar=('PYTHON_FILE', 'PYTHON_FILE'), help='Adds functions contained in Python files. See the Additional Python function format section of the documentation for more details.')

    parser.add_argument('--version', action='store_true', dest='version', help='Only prints the version.')

    return parser.parse_args()


VERSION = '1.0.0'


if __name__ == '__main__':
    parameters = read_parameters()

    if parameters.version:
        print(VERSION)
        exit()

    retrieve_constants(parameters)
    retrieve_expressions(parameters)
    parameters.regression_expression = get_default_regression_expression(parameters.regression_expression)

    try:
        plot(parameters)
    except KeyboardInterrupt:
        print('\n\nInterrupted by user.')
