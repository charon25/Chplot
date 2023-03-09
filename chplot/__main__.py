import argparse

from chplot.plot import plot


def read_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="TODO")
    parser.add_argument('expressions', metavar='EXPRESSION', nargs='+', help='The expression(s) to plot.')
    parser.add_argument('-v', metavar='VARIABLE', dest='variable', help="The name of the variable plotted on the x-axis (default: 'x').")
    parser.add_argument('-x', nargs=2, metavar=('X_MIN', 'X_MAX'), type=float, dest='x_lim', help='The x-axis bounds (default: [0, 1]).')
    parser.add_argument('-xlog', action='store_true', dest='is_x_log', help="Indicate if the x-axis scale should be logarithmic.")
    parser.add_argument('-y', nargs=2, metavar=('Y_MIN', 'Y_MAX'), type=float, dest='y_lim', help='The y-axis bounds (default: adjust to the graphs).')
    parser.add_argument('-z', action='store_true', dest='must_contains_zero', help='Indicate if the y-axis should contain zero. If the -y parameter is present, it will be overriden as necessary.')
    parser.add_argument('-ylog', action='store_true', dest='is_y_log', help="Indicate if the y-axis scale should be logarithmic.")
    parser.add_argument('-n', metavar='POINTS', type=int, dest='n_points', help='Number of points for each expression (default: 10000).')
    parser.add_argument('-i', action='store_true', dest='is_integer', help='Indicate if the inputs should be forced as integers. Will have at most POINTS points, but it may have less if the x-axis bounds are too close.')

    return parser.parse_args()


if __name__ == '__main__':
    parameters = read_parameters()
    print(parameters)

    plot(parameters)

