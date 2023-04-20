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

#### Important note

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

No option is mandatory.

|<div style="width:125px">CLI options</div>|`PlotParameters` class equivalent |Expected arguments |Effect |
|---------------------|--------------------------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|$\emptyset$ |expressions: list[str] |Any number of expressions (including none of them) |The expressions of the mathematical functions to plot and do computations on. There can by none of them. |
|`-v`<br>`--variable` |variable: str |One string |The variable going of the horizontal axis. Can be more than one character. Defaults to `x`. |
|`-n`<br>`--n-points` |n_points: int |One positive integer (excluding zero) |The number of points on the horizontal axis for the plotting of the expressions. Defaults to 10001. |
|`-i`<br>`--integers` |is_integer: bool |$\emptyset$ |Forces the points where the expressions are computed to be integers between the specified limits. Defaults to False. |
|`-x`<br>`--x-lim` |x_lim: tuple[float&#124;str&#124;None, float&#124;str&#124;None]|Two expressions |The horizontal axis bounds where the expression are computed. First argument is the min, second is the max. Any expression (such as `2pi` or `1+exp(2)`) is valid. It is also the graph default horizontal axis, but they can be modified to accomodate other data. Defaults to `0 1`. |
|`-xlog`<br>`--xlog` |is_x_log: bool |$\emptyset$ |Forces a logarithmic scale on the horizontal axis. If some horizontal axis bounds are ? 0, will modify them. Defaults to False. |
|`-y`<br>`--y-lim` |y_lim: tuple[float&#124;str&#124;None, float&#124;str&#124;None]|Two expressions |The vertical axis bounds of the graph. First argument is the min, second is the max. Any expression (such as `2pi` or `1+exp(2)`) is valid. If not specified, will use matplotlib default ones to accomodate all data. Will restrict the graph to them is specified. |
|`-z`<br>`--y-zero` |must_contain_zero: bool |$\emptyset$ |Forces the vertical axis to contain zero. Defaults to False. |
|`-ylog`<br>`--ylog` |is_y_log: bool |$\emptyset$ |Forces a logarithmic scale on the vertical axis. If some vertical axis bounds are ? 0, will modify them. Defaults to False. |
|`-xl`<br>`--x-label` |x_label: str |One string |Label of the horizontal axis. Defaults to nothing. |
|`-y`<br>`--y-label` |y_label: str |One string |Label of the vertical axis. Defaults to nothing. |
|`-t`<br>`--title` |title: str |One string |Title of the graph. Defaults to nothing. |
|`-rl`<br>`--remove-legend`|remove_legend: bool |$\emptyset$ |Removes the graph legend. Defaults to False. |
|`--no-plot` |no_plot: bool |$\emptyset$ |Does not show the plot. However, does not prevent saving the figure. Defaults to False. |
|`--dis`<br>`--discontinuous` |markersize: int&#124;None |One optional positive integer (excluding zero) |Transforms the style of the graph from a continuous line to discrete points with the specified radius. If present without a value, will defaults to a radius of 1. If the `--integer` flag is also present, will still affect the points radius. |
|`-c`<br>`--constants` |constants: list[str] |One string or more, either a filepath or of the forme `<name>=<expression>`|Adds constants which may be used by any other expressions (including axis bounds). They must either be of the form `<name>=<expression>` (eg `a=4sin(pi/4)`) or be filepath containing lines respecting this format. Note that filepaths are only accepted in the CLI. May override already existing constants and functions. If a constant refers to another one, it should be defined after. Defaults to nothing. |
|`-f`<br>`--file` |data_files: list[str] |One or more filepaths |Adds data contained in CSV files as new functions to the graph. See the [CSV files format](#cli-files-format) section for more details. Defaults to nothing. |
|`-s`<br>`--save-graph` |save_figure_path: str |One filepath |Saves the graph at the specified path. If not included, will not save the figure (default behavior). |
|`-d`<br>`--save-data` |save_data_path: str |One filepath |Saves the graph data (x and y values) at the specified path in CSV format. If not included, will not save the data (default behavior). |
|`-p`<br>`--python-file`|python_files: list[str] |One or more filepaths |Adds functions contained in Python files. See the [Additional Python function format](#additional-python-function-format) for more details. Defaults to nothing. |
|`--zeros` |zeros_file: str&#124;None |One optional filepath |Computes where the expressions equal zero. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file. |
|`--int`<br>`--integral`|integral_file: str&#124;None |One optional filepath |Computes the integral of all functions on the entire interval where it is plotted. Note that it does **not** add the antideritive of the functions to the graph, but only computes the area under them on their definition interval. If not included, will not compute it (default behavior), else if included without argument, prints the results to the console, else writes it to the given file. |
|`--deriv`<br>`--derivative`|derivation_orders: list[int] |At least one positive integer (excluding zero) |Computes and adds to the graph the derivative of the specified orders of every other function. Note that the higher the order, the more inaccuracy and unstability it has. Furthermore, the derivative computation will shave off a few points on each side, so the derivatives are defined on a smaller interval. |
|`--reg`<br>`--regression`|regression_expression: str |One expression |Computes the coefficients of the given regression to get the best fit to every other function. The regression parameters should have the form `_rX` where X is any string made of digits, letters and underscores and starting with a letter (eg `_ra0`). The regression will also be added in the final graph. When using the CLI, the expression can also be one of a few default keywords (listed in [Regression default keywords](#regression-default-keywords)).|

### Options synergies

Every option that computes something based on the functions will act on every function defined before it applies. The order of application is the following (each item applies to all the previous ones):
- Base expressions & file data
- Regressions
- Derivations
- Integrals & zeros

For instance, this means every regression will also be derivated, and every derivative will be integrated.

### CSV files format

The `--file` option will accept any CSV file respecting those rules:
- the column delimiter is eitehr a comma (`,`), a semicolon (`;`), a space (` `) or a tabulation (`\t`) ;
- the decimal separator is either a dot (`.`) or a comma (`,`) if the column delimiter is something else (for countries and language using them, such as French or German) ;
- text entry containing the column delimiter must be surrounded by double quotes (`"`) ;
- to have double quotes (`"`) in a text entry, just double them (`""`).

The first column will be considered the horizontal axis data for the entire file. Each subsequent column will be a new function. They might all be of different lengths, and some value may be missing. Any missing value in the first column will ignore the whole line.

The first non numerical line will be used as label for the functions.

#### Examples

The file
```csv
x,"First y","Second ""y""",ThirdY,EmptyColumn
0,0,,0,
1,10,100,,
2,20,,2000,
3,30,300,3000,
4,40,400,,
```
Will result in the following functions (represented as (x,y) couples):
- `First y`: (0, 0), (1, 10), (2, 20), (3, 30), (4, 40)
- `Second "y"`: (1, 100), (3, 300), (4, 400)
- `ThirdY`: (0, 0), (2, 2000), (3, 3000)

Note that the last column does not have any values, so it won't be registered at all.

The file
```csv
x;y1;y2
0,0;1,0;2,1
0,3;1,2;2,5
0,6;1,55;2,123
1;1,825;2,99
```
Will result in the following functions:
- `y1`: (0, 1), (0.3, 1.2), (0.6, 1.55), (1, 1.825)
- `y2`: (0, 2.1), (0.3, 2.5), (0.6, 2.123), (1, 2.99)


### Regression default keywords

When using Chplot from the command line and using the `--regression` command, a keyword can be specified instead of an expression to get usual regression expression. Those keywords are listed below :

|Keyword|<div style="width:300px">Mathematical function</div>|Equivalent expression|
|-------|:-------------------:|:-------------------:|
|`const`<br>`constant`| $f(x) = m$ |`_rm`|
|`lin`<br>`linear`| $f(x) = ax + b$ |`_ra * x + _rb`|
|`pN`<br>`polyN`<br>`polynomialN`<br>where $N \in \mathbb{N} $ | $$f(x) = \sum_{i=0}^N a_i x^i$$ |`_ra0`<br>`_ra1 * x + _ra0`<br>`_ra2 * x^2 + _ra1 * x + _r0`<br>`...`|
|`power`| $f(x) = k x^\alpha$ |`_rk * x^_ralpha`|
|`powery`| $f(x) = k x^\alpha + y_0$ |`_rk * x^_ralpha + r_y0`|
|`log`| $f(x) = a \ln(x) + b$ |`_ra * ln(x) + _rb`|
|`exp`| $f(x) = a \mathrm{e}^{bx}$ |`_ra * exp(x * _rb)`|
|`expy`| $f(x) = a \mathrm{e}^{bx} + y_0$ |`_ra * exp(x * _rb) + _ry0`|

Note that `poly0` is equivalent to `constant` and `poly1` is equivalent to `linear`.

### Additional Python function format

Chplot expression can accept functions usable in any expression directly from other Python files. Those file must respect those rules:
- they must be in the same directory as the console when using the CLI (and in the same directory as the python execution when using the code version [NOT TESTED]) ;
- all functions to add must be decorated with the `@plottable` decorator (importable with `from chplot import plottable`). The decorator **must** indicate how many arguments is expected by the function, either directly or with the `arg_count` keyword (i.e. `@plottable(1)` or `@plottable(arg_count=2)`) ;
- all functions must only accept `int` or `float` and must only return **one** value accepted by the `float()` built-in function of Python, such as `int`, `float` or `bool` (if not, will be considered as the same as a raised Exception) ;
- to indicate an error in the computation (such as a division by zero or the square root of a negative number), the function can either raise an exception or return `math.nan` (or `float('nan')`). Note that an exception will completely stop the computation at that point while `nan` will be used in the rest of the expression, which may change the result slightly.

Everything other than those rules is allowed, such as importing other modules.
The name of the Python function will be the same as the name used in the expression.

#### Examples

The Python file `functions.py`
```python
from chplot import plottable
import math

@plottable(1)
def inc(x: float) -> float:
 return x + 1

@plottable(arg_count=2)
def invradius(x: float, y: float) -> float:
 if x == y == 0:
 raise ZeroDivisionError
 
 return 1 / math.sqrt(x * x + y * y)

def dec(x: float) -> float:
 return x - 1

@plottable
def double(x: float) -> float:
 return x * 2
```
Will define **2** new functions usable in expression: `inc` and `invradius`. `dec` does not have the decorator and will be ignored, and `double` does not indicate how many parameters it accepts, and therefore will also be ignored (but a Warning will be logged).

This means, the following command is valid:
```bash
python -m chplot "inc(invradius(x, 5))" -x 1 inc(2) -p functions.py
```

## Available functions

Chplot is bundled by default with almost 40 mathematical and physical constants and over 200 mathematical functions from the default `math` module, `mpmath`, `scipy.special` as well as custom made ones. They are all described in the following sections. The documentation of functions from `math` or the third-party modules can be found in their respective wikis: [math](https://docs.python.org/3/library/math.html), [scipy.special](https://docs.scipy.org/doc/scipy/reference/special.html), [mpmath](https://mpmath.org/doc/current/).

There are also the 5 base operations : `+`, `-`, `*`, `/`, `^`.

### Constants

`nan` and `_` are valid constants that both evaluates to `math.nan`. They can be used to remove some points from the graph (for instance with the `if` or `in` functions, see below).

#### Mathematical constants

|`chplot` name|Name |Usual symbol|Exact value|`chplot` value |
|-------------|---------------------------|:----------:|:---------:|:---------------:|
|`pi` |Pi | $\pi$ | $\pi$ |$3.141\ 592\ 653\ 589\ 793$|
|`tau` |Tau | $\tau$ | $2\pi$ |$6.283\ 185\ 307\ 179\ 586$|
|`e` |Euler's number | $e$ | $$\exp(1) = \sum_{n=0}^{+\infty} \frac{1}{n!}$$ |$2.718\ 281\ 828\ 459\ 045$|
|`ga`<br>`em` |Euler-Mascheroni's constant| $\gamma$| $$\lim_{n\to\infty} \left( \sum_{k=1}^n \left( \frac{1}{k}\right) - \log n \right)$$ |$0.577\ 215\ 664\ 901\ 532 9$|
|`phi` |Golden ratio | $\phi$ | $\frac{1}{2} (1 + \sqrt{5})$ |$1.618\ 033\ 988\ 749\ 895$|
|`sqrt2` |Square root of 2 | $\sqrt{2}$ | $\sqrt{2}$ |$1.414\ 213\ 562\ 373\ 095\ 1$|
|`apery` |Apery's constant || $$\zeta(3) = \sum_{n=1}^{+\infty} \frac{1}{n^3} $$ |$1.202\ 056\ 903\ 159\ 594$|
|`brun` |Brun's constant| $B_2$ |Sum of the reciprocal of the twin primes|$1.902\ 160\ 583\ 104$|
|`catalan` |Catalan's constant | $G$ | $$\sum_{n=0}^{+\infty} \frac{(-1)^n}{(2n + 1)^2} $$ |$0.915\ 965\ 594\ 177\ 219$|
|`feigenbaumd`|First Feigenbaum's constant| $\delta$ | |$4.669\ 201\ 609\ 102\ 990\ 67$|
|`feigenbauma`|Second Feigenbaum's constant| $\alpha$ | |$2.502\ 907\ 875\ 095\ 892\ 82$|
|`glaisher` |Glaisher-Khinkelin's constant| $A$ | $$\lim_{n\to\infty} \frac{\Pi_{k=1}^{n} k^k}{n^{\frac{n^2}{2} + \frac{n}{2} + \frac{1}{12}}\cdot\mathrm{e}^{-\frac{n^2}{4}}}$$ |$1.282\ 427\ 129\ 100\ 622\ 6$|
|`khinchin` |Khinchin's constant| $K_0$ | $$\prod_{r=1}^{+\infty} \left(1 + \frac{1}{r(r+2)} \right)^{\log_2 r}$$|$2.685\ 452\ 001\ 065\ 306\ 2$|
|`mertens` |Meissel-Mertens's constant| $M$ | $$\gamma + \sum_{p\text{ prime}}\left(\ln\left(1 - \frac{1}{p}\right) + \frac{1}{p} \right)$$ |$0.261\ 497\ 212\ 847\ 642\ 77$|

#### Physical constants

The constants, their values and their units are taken from https://en.wikipedia.org/wiki/List_of_physical_constants.

|`chplot` name|Quantity|Symbol|`chplot` value (in SI units)|Units|
|-------------|----|:----:|:------------:|:---:|
|`a0`       |Bohr's radius| $a_0$ | $5.291\ 772\ 109\ 03\times10^{-11}$ | $\text{m}$ |
|`alpha`    |Fine-structure constant| $\alpha$ | $7.297\ 352\ 569\ 3\times10^{-3}$ | --- |
|`b`        |Wien's wavelength displacement law constant| $b$ | $2.897\ 771\ 955\times10^{-3}$ | $\text{m}\cdot\text{K}$ |
|`bp`       |Wien's entropy displacement law constant| $b_{\text{entropy}}$ | $3.002\ 916\ 077\times10^{-3}$ | $\text{m}\cdot\text{K}$ |
|`bp`       |Wien's frequency displacement law constant| $b'$ | $5.878\ 925\ 757\times10^{10}$ | $\text{Hz}\cdot\text{K}^{-1}$ |
|`c`        |Speed of light in vacuum| $c$ | $2.997\ 924\ 58\times10^8$ | $\text{m}\cdot\text{s}^{-1}$ |
|`c1`       |First radiation constant| $c_1$ | $3.741\ 771\ 852\times10^{-16}$ | $\text{W}\cdot\text{m}^2$ |
|`c1L`      |Second radiation constant | $c_{1L}$ | $1.191\ 042\ 972\ 397\ 188\times10^{-16}$ | $\text{W}\cdot\text{m}^2\cdot\text{sr}^{-1}$ |
|`c2`       |Second radiation constant| $c_2$ | $1.438\ 776\ 877\times10^{-2}$ | $\text{m}\cdot\text{K}$ |
|`dnuCs`    |Hyperfine transistion frequency of Cesium-133| $\Delta\nu_{\text{Cs}}$ | $9.192\ 631\ 770\times10^{9}$ | $\text{Hz}$ |
|`ec`       |Elementary charge| $e$ | $1.602\ 176\ 634\times10^{-19}$ | $\text{C}$ |
|`Eh`       |Hartree's energy| $E_h$ | $4.359\ 744\ 722\ 207\ 1\times10^{-18}$ | $\text{J}$ |
|`epsilon0`<br>`eps0` |Vacuum electric permittivity    | $\varepsilon_0$ | $8.854\ 187\ 812\ 8\times10^{-12}$ | $\text{F}\cdot\text{m}^{-1}$ |
|`F`        |Faraday's constant| $F$ | $9.648\ 533\ 212\ 331\ 002\times10^4$ | $\text{C}\cdot\text{mol}^{-1}$ |
|`G`        |Gravitational constant| $G$ | $6.674\ 3\times10^{-11}$ | $\text{m}^3\cdot\text{kg}^{-1}\cdot\text{s}^{-2}$ |
|`g`        |Gravity of Earth| $g$ | $9.806\ 65$ | $\text{m}\cdot\text{s}^{-2}$ |
|`G0`       |Conductance quantum| $G_0$ | $7.748\ 091\ 729\times10^{-5}$ | $\text{S}$ |
|`ge`       |Electron g-factor| $g_e$ | $-2.002\ 319\ 304\ 362\ 56$ | --- |
|`GF0`      |Fermi coupling constant<br>Reduced Fermi constant| $$G^0_F$$ | $4.543\ 795\ 7\times10^{14}$ | $\text{J}^{-2}$ |
|`gmu`      |Muon g-factor| $g_\mu$ | $-2.002\ 331\ 841\ 8$ | --- |
|`gP`       |Proton g-factor| $g_P$ | $5.585\ 694\ 689\ 3$ | --- |
|`h`        |Planck's constant| $h$ | $6.626\ 070\ 15\times10^{-34}$ | $\text{J}\cdot\text{Hz}^{-1}$ |
|`hb`       |Reduced Planck's constant | $\hbar$ | $1.054\ 571\ 817\times10^{-34}$ | $\text{J}\cdot\text{s}$ |
|`kB`       |Boltzmann's constant    | $k$, $k_B$ | $1.380\ 649\times10^{-23}$ | $\text{J}\cdot\text{K}^{-1}$ |
|`ke`       |Coulomb's constant    | $k_e$ | $8.987\ 551\ 792\ 3\times10^9$ | $\text{N}\cdot\text{m}^2\cdot\text{C}^{-2}$ |
|`KJ`       |Josephson's constant| $K_J$ | $4.835\ 978\ 484\times10^{14}$ | $\text{Hz}\cdot\text{V}^{-1}$ |
|`m12C`     |Atomic mass of carbon-12| $m(^{12}\text{C})$ | $1.992\ 646\ 879\ 92\times10^{26}$ | $\text{kg}$ |
|`M12C`     |Molar mass of carbon-12| $M(^{12}\text{C})$ | $1.199\ 999\ 999\ 58\times10^{-2}$ | $\text{kg}\cdot\text{mol}^{-1}$ |
|`me`       |Electron mass| $m_e$ | $9.109\ 383\ 701\ 5\times10^{-31}$ | $\text{kg}$ |
|`mmu`      |Muon mass| $m_\mu$ | $1.883\ 531\ 627\times10^{-28}$ | $\text{kg}$ |
|`mn`       |Neutron mass| $m_n$ | $1.674\ 927\ 498\ 04\times10^{-27}$ | $\text{kg}$ |
|`mp`       |Proton mass| $m_p$ | $1.672\ 621\ 923\ 69\times10^{-27}$ | $\text{kg}$ |
|`mt`       |Top quark mass| $m_t$ | $3.078\ 4\times10^{-25}$ | $\text{kg}$ |
|`mtau`     |Tau mass| $m_\tau$ | $3.167\ 54\times10^{-27}$ | $\text{kg}$ |
|`mu`       |Atomic mass constant| $m_u$ | $1.660\ 539\ 066\ 6\times10^{-27}$ | $\text{kg}$ |
|`Mu`       |Molar mass constant| $M_u$ | $9.999\ 999\ 996\ 5\times10^{-4}$ | $\text{kg}\cdot\text{mol}^{-1}$ |
|`mu0`      |Vacuum magnetic parmeability    | $\mu_0$ | $1.256\ 637\ 602\ 12\times10^{-6}$ | $\text{N}\cdot\text{A}^{-2}$ |
|`muB`      |Bohr's magneton| $\mu_B$ | $9.274\ 010\ 078\ 3\times10^{-24}$ | $\text{J}\cdot\text{T}^{-1}$ |
|`muN`      |Nuclear magneton| $\mu_N$ | $5.050\ 783\ 746\ 1\times10^{-27}$ | $\text{J}\cdot\text{T}^{-1}$ |
|`NA`       |Avogadro constant| $N_A$ | $6.022\ 140\ 76\times10^{23}$ | $\text{mol}^{-1}$ |
|`R`        |Molar gas constant| $R$ | $8.314\ 462\ 618\ 153\ 24$ | $\text{J}\cdot\text{mol}^{-1}\cdot\text{K}^{-1}$ |
|`re`       |Classical electron radius| $r_e$ | $2.817\ 940\ 326\ 2\times10^{-15}$ | $\text{m}$ |
|`Rinf`     |Rydberg's constant| $R_\infty$ | $1.097\ 373\ 156\ 816\times10^7$ | $\text{m}^{-1}$ |
|`RK`       |Von Klitzing's constant| $R_K$ | $2.581\ 280\ 745\times10^{4}$ | $\Omega$ |
|`Ry`       |Rydberg's unit of energy| $R_y$ | $2.179\ 872\ 361\ 103\ 5\times10^{-18}$ | $\text{J}$ |
|`sigma`    |Stefan-Boltzmann's constant| $\sigma$ | $5.670\ 374\ 419\times10^{-8}$ | $\text{W}\cdot\text{m}^{-2}\cdot\text{K}^{-4}$ |
|`sigmae`   |Thomson's cross section| $\sigma_e$ | $6.652\ 458\ 732\ 1\times10^{-29}$ | $\text{m}^2$ |
|`VmSi`     |Molar volume of silicon| $V_m(\text{Si})$ | $1.205\ 883\ 199\times10^{-5}$ | $\text{m}^3\cdot\text{mol}^{-1}$ |
|`Z0`       |Characteristic impedance of vacuum    | $Z_0$ | $376\ .730\ 313\ 668\ $ | $\Omega$ |



### From default `math` module

Documentation : https://docs.python.org/3/library/math.html

| `chplot` name(s) | `math` name | Number of arguments | Notes |
|:---------------------:|:-------------:|:-------------------:|:-----:|
| `acos` | `acos` | 1 | |
| `acosh` | `acosh` | 1 | |
| `asin` | `asin` | 1 | |
| `asinh` | `asinh` | 1 | |
| `atan` | `atan` | 1 | |
| `atanh` | `atanh` | 1 | |
| `atan2` | `atan2` | 2 | |
| `cbrt` | `cbrt` | 1 | |
| `ceil` | `ceil` | 1 | |
| `copysign` | `copysign` | 2 | |
| `cos` | `cos` | 1 | |
| `cosh` | `cosh` | 1 | |
| `degrees` | `degrees` | 1 | |
| `erf` | `erf` | 1 | |
| `erfc` | `erfc` | 1 | |
| `exp` | `exp` | 1 | |
| `expm1` | `expm1` | 1 | |
| `floor` | `floor` | 1 | |
| `fmod` | `fmod` | 2 | |
| `gamma` | `gamma` | 1 | |
| `hypot` | `hypot` | 2 | |
| `lgamma`<br>`lngamma` | `lgamma` | 1 | |
| `log`<br>`ln` | `log` | 1 | |
| `log10` | `log10` | 1 | |
| `log1p` | `log1p` | 1 | |
| `log2` | `log2` | 1 | |
| `radians` | `radians` | 1 | |
| `remainder` | `remainder` | 2 | |
| `sin` | `sin` | 1 | |
| `sinh` | `sinh` | 1 | |
| `sqrt` | `sqrt` | 1 | |
| `tan` | `tan` | 1 | |
| `trunc` | `trunc` | 1 | |


### From `mpmath`

### From `scipy.special`

### Probability functions

### Other functions


## Graph and computations examples

