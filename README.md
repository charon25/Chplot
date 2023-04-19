# Chplot - Arbitrary functions plotting and computations

Chplot is a Python >= 3.9 module to plot any arbitrary mathematical expressions as well as data series from files, and compute its derivatives and integrals, where it equals zero, and much more!

## Installation

You can install `chplot` through Pypi, with the command:
```bash
python -m pip install chplot
```

You can also install it by cloning this repo and installing it directly:
```bash
git clone https://github.com/charon25/Chplot.git
cd Chplot
python -m pip install .
```

To check it is properly installed, just run and check it outputs the current version:
```bash
python -m chplot --version
```

This module requires the following third-party modules:
- matplotlib >= 3.6.1
- mpmath >= 1.2.1
- numpy >= 1.23.4
- scipy >= 1.9.3
- [shuting_yard](https://pypi.org/project/shunting-yard/) >= 1.0.9
- tqdm >= 4.64.1

## Usage

In the rest of this README, the term "expression" will refer to any mathematical expression that is the function of one variable (by default `x` but can be changed).

### CLI

This module is primarly intended to be used in the command-line. To do this, use the following command:
```bash
python -m chplot [expression1, [expression2, ...]] [additional-parameters...]
```

Where all the additional parameters are documented in the [CLI options](#cli-options) section.

==/!\\ Important note /!\\==
Due to the working of the `argparse` Python module and the majority of shells, you may have to surround any expression with double quotes (`"`) if it contains a caret (`^`). Furthermore, if it starts with a dash (`-`) you may also need to add a space or a `0` before it.
For instance, you need to write `" -x"` or `"0-x"` to get the function `f(x) = -x` and `"x^2"` (instead of just `x^2`) to get the square function.

### From Python code

The `chplot` module can also be used from another program. Sample codes:
```python
# Use this to use the built-in parameters class
import chplot

parameters = chplot.PlotParameters()
plot(parameters)
```

```python
# Use this to use another class and set default values
import chplot

parameters = ... # any object
chplot.set_default_values(parameters) # add any missing field with its default value

plot(parameters)
```

All the `PlotParameters` arguments are summarized in the [CLI options](#cli-options) section.

### CLI options

|CLI options          |`PlotParameters` equivalent                 |Expected arguments                                                         |Effect                                                                                                                                                                                                                                                                                                                                                                                                         |
|---------------------|--------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|$\emptyset$          |expressions: list[str]                      |Any number of expressions                                                  |The expressions of the mathematical functions to plot and do computations on. There can by none of them.                                                                                                                                                                                                                                                                                                       |
|`-v`<br>`--variable`  |variable: str                               |One string                                                                 |The variable going of the horizontal axis. Can be more than one character. Defaults to `x`.                                                                                                                                                                                                                                                                                                                    |
|`-n`<br>`--n-points`   |n_points: int                               |One positive integer (excluding zero)                                      |The number of points on the horizontal axis for the plotting of the expressions. Defaults to 10001.                                                                                                                                                                                                                                                                                                            |
|`-i`<br>`--integers`   |is_integer: bool                            |$\emptyset$                                                                |Forces the points where the expressions are computed to be integers between the specified limits. Defaults to False.                                                                                                                                                                                                                                                                                           |
|`-x`<br>`--x-lim`      |x_lim: tuple[float&#124;str&#124;None, float&#124;str&#124;None]|Two expressions                                                            |The horizontal axis bounds where the expression are computed. First argument is the min, second is the max. Any expression (such as `2pi` or `1+exp(2)`) is valid. It is also the graph default horizontal axis, but they can be modified to accomodate other data. Defaults to `0 1`.                                                                                                                         |
|`-xlog`<br>`--xlog`    |is_x_log: bool                              |$\emptyset$                                                                |Forces a logarithmic scale on the horizontal axis. If some horizontal axis bounds are ? 0, will modify them. Defaults to False.                                                                                                                                                                                                                                                                                |
|`-y`<br>`--y-lim`      |y_lim: tuple[float&#124;str&#124;None, float&#124;str&#124;None]|Two expressions                                                            |The vertical axis bounds of the graph. First argument is the min, second is the max. Any expression (such as `2pi` or `1+exp(2)`) is valid. If not specified, will use matplotlib default ones to accomodate all data. Will restrict the graph to them is specified.                                                                                                                                           |
|`-z`<br>`--y-zero`     |must_contain_zero: bool                     |$\emptyset$                                                                |Forces the vertical axis to contain zero. Defaults to False.                                                                                                                                                                                                                                                                                                                                                   |
|`-ylog`<br>`--ylog`    |is_y_log: bool                              |$\emptyset$                                                                |Forces a logarithmic scale on the vertical axis. If some vertical axis bounds are ? 0, will modify them. Defaults to False.                                                                                                                                                                                                                                                                                    |
|`-xl`<br>`--x-label`   |x_label: str                                |One string                                                                 |Label of the horizontal axis. Defaults to nothing.                                                                                                                                                                                                                                                                                                                                                             |
|`-y`<br>`--y-label`    |y_label: str                                |One string                                                                 |Label of the vertical axis. Defaults to nothing.                                                                                                                                                                                                                                                                                                                                                               |
|`-t`<br>`--title`      |title: str                                  |One string                                                                 |Title of the graph. Defaults to nothing.                                                                                                                                                                                                                                                                                                                                                                       |
|`-rl`<br>`--remove-legend`|remove_legend: bool                         |$\emptyset$                                                                |Removes the graph legend. Defaults to False.                                                                                                                                                                                                                                                                                                                                                                   |
|`--no-plot`          |no_plot: bool                               |$\emptyset$                                                                |Does not show the plot. However, does not prevent saving the figure. Defaults to False.                                                                                                                                                                                                                                                                                                                        |
|`--dis`              |plot_without_lines: bool                    |$\emptyset$                                                                |Removes the lines between each point of the graph. Does nothing if the --integer flag is present. Defaults to False.                                                                                                                                                                                                                                                                                           |
|`-c`<br>`--constants`  |constants: list[str]                        |One string or more, either a filepath or of the forme `<name>=<expression>`|Adds constants which may be used by any other expressions (including axis bounds). They must either be of the form `<name>=<expression>` (eg `a=4sin(pi/4)`) or be filepath containing lines respecting this format. Note that filepaths are only accepted in the CLI. Defaults to nothing.                                                                                                                    |
|`-f`<br>`--file`       |data_files: list[str]                       |One or more filepaths                                                      |Adds data contained in CSV files. See the [CSV files format](#cli-files-format) section for more details. Defaults to nothing.                                                                                                                                                                                                                                                                                 |
|`-s`<br>`--save-graph` |save_figure_path: str                       |One filepath                                                               |Saves the graph at the specified path. If not included, will not save the figure (default behavior).                                                                                                                                                                                                                                                                                                           |
|`-d`<br>`--save-data`  |save_data_path: str                         |One filepath                                                               |Saves the graph data (x and y values) at the specified path in CSV format. If not included, will not save the data (default behavior).                                                                                                                                                                                                                                                                         |
|`-p`<br>`--python-file`|python_files: list[str]                     |One or more filepaths                                                      |Adds functions contained in Python files. See the [Additional Python function format](#additional-python-function-format) for more details. Defaults to nothing.                                                                                                                                                                                                                                               |
|`--zeros`            |zeros_file: str&#124;None                        |One optional filepath                                                      |Computes where the expressions equal zero. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file.                                                                                                                                                                                                    |
|`--int`<br>`--integral`|integral_file: str&#124;None                     |One optional filepath                                                      |Computes the integral of the function on the entire interval where it is plotted. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file.                                                                                                                                                             |
|`--deriv`<br>`--derivative`|derivation_orders: list[int]                |At least one positive integer (excluding zero)                             |Computes and adds to the graph the derivative of the specified orders of every other function.                                                                                                                                                                                                                                                                                                                 |
|`--reg`<br>`--regression`|regression_expression: str                  |One expression                                                             |Computes the coefficients of the given regression to get the best fit to every other function. The regression parameters should have the form `_rX` where X is any string made of digits, letters and underscores and starting with a letter (eg `_ra0`). When using the CLI, the expression can also be one of a few default keywords (listed in [Regression default keywords](#regression-default-keywords)).|


## Available functions

## Examples

