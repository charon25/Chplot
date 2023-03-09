import argparse

from chplot.plot import plot


def read_parameters() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('expressions', metavar='EXPRESSION', nargs='+', help='The expression(s) to plot.')
    parser.add_argument('-v', metavar='VARIABLE', dest='variable', help="The name of the variable plotted on the x-axis (default: 'x').")
    parser.add_argument('-x', nargs=2, metavar=('X_MIN', 'X_MAX'), type=float, dest='x_lim', help='The x-axis limits (default: [0, 1]).')
    parser.add_argument('-n', metavar='POINTS', type=int, dest='n_points', help='Number of points for each expression (default: 10000).')

    return parser.parse_args()


if __name__ == '__main__':
    parameters = read_parameters()
    print(parameters)

    plot(parameters)

