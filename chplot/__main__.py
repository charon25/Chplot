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


def read_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument('expressions', metavar='EXPRESSION', nargs='*', help='The expression(s) to plot. Can also be files containing expressions.')
    parser.add_argument('-v', metavar='VARIABLE', dest='variable', help="The name of the variable plotted on the x-axis (default: 'x').")
    parser.add_argument('--no-sn', action='store_true', dest='disable_scientific_notation', help="Disable auto-conversion of scientific notation.")

    parser.add_argument('-n', metavar='POINTS', type=positive_integer, dest='n_points', help='Number of points for each expression (default: 10001).')
    parser.add_argument('-i', action='store_true', dest='is_integer', help='Indicate if the inputs should be forced as integers. Will have at most POINTS points, but it may have less if the x-axis bounds are too close.')

    parser.add_argument('-x', nargs=2, metavar=('X_MIN', 'X_MAX'), dest='x_lim', help='The x-axis bounds (default: [0, 1]). Any mathematical expression is valid as long as it is constant.')
    parser.add_argument('-xlog', action='store_true', dest='is_x_log', help="Indicate if the x-axis scale should be logarithmic.")

    parser.add_argument('-y', nargs=2, metavar=('Y_MIN', 'Y_MAX'), dest='y_lim', help='The y-axis bounds (default: adjust to the graphs). Any mathematical expression is valid as long as it is constant.')
    parser.add_argument('-z', action='store_true', dest='must_contain_zero', help='Indicate if the y-axis should contain zero. If the -y parameter is present, it will be overriden as necessary.')
    parser.add_argument('-ylog', action='store_true', dest='is_y_log', help="Indicate if the y-axis scale should be logarithmic.")

    parser.add_argument('-xl', metavar='X_LABEL', dest='x_label', help='The x-axis label.')
    parser.add_argument('-yl', metavar='Y_LABEL', dest='y_label', help='The y-axis label.')
    parser.add_argument('-t', metavar='TITLE', dest='title', help='The plot title.')
    parser.add_argument('-rl', action='store_true', dest='remove_legend', help='Remove the plot legend.')
    parser.add_argument('--no-plot', action='store_true', dest='no_plot', help='If present, will not graph the functions at all.')
    parser.add_argument('--dis', nargs='?', const=1, type=positive_integer, dest='markersize', help='Remove line segment between points. Does nothing if the -i flag is present.')

    parser.add_argument('--zeros', nargs='?', const=0, dest='zeros_file', help='Indicate if the zeros of the functions should be computed. If no arguments are provided, will write to stdout, otherwise to the specified file.')
    parser.add_argument('--integral', nargs='?', const=0, dest='integral_file', help='Indicate if the integral of the functions should be computed. If no arguments are provided, will write to stdout, otherwise to the specified file.')
    parser.add_argument('--deriv', nargs='+', dest='derivation_orders', type=positive_integer, help='Will add the derivative to the graph (and integral/zeros computation).')
    parser.add_argument('--reg', dest='regression_expression', metavar='REGRESSION_EXPRESSION', help='Compute the best coefficients to get the best fit of file data series with the given expression. The coefficients must be of the form _rx where x is any string.')

    parser.add_argument('-c', nargs='+', dest='constants_arg', metavar=('CONSTANT', 'CONSTANT'), help='Constants to add to the computation, at least one and as much as needed. Either of the form "<name>=<expression>", or the name of a file containing this form of statement, one on each line.')
    parser.add_argument('-f', nargs='+', dest='data_files', metavar=('CSV_FILE', 'CSV_FILE'), help='Filenames of CSV files to add points.')
    parser.add_argument('-s', dest='save_figure_path', metavar='FIGURE_FILE', help='Save figure to file.')
    parser.add_argument('-d', dest='save_data_path', metavar='DATA_FILE', help='Save all points to a csv file.')
    parser.add_argument('-p', nargs='+', dest='python_files', metavar=('PYTHON_FILE', 'PYTHON_FILE'), help='Python file contaning @plottable decorated functions that can be used in the ploting step.')

    parser.add_argument('--version', action='store_true', dest='version', help='Print the version.')

    return parser.parse_args()


if __name__ == '__main__':
    parameters = read_parameters()

    if parameters.version:
        print('1.0.0')
        exit()

    retrieve_constants(parameters)
    retrieve_expressions(parameters)
    parameters.regression_expression = get_default_regression_expression(parameters.regression_expression)

    try:
        plot(parameters)
    except KeyboardInterrupt:
        print('\n\nInterrupted by user.')
