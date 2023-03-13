import math

from chplot.functions.utils import FunctionDict


_MATH_CONSTANTS: FunctionDict = {
    'pi': (0, math.pi),
    'tau': (0, 2 * math.pi),
    'e': (0, math.e),
    'ga': (0, 0.577_215_664_901_532_9),
    'em': (0, 0.577_215_664_901_532_9),
    'phi': (0, 1.618_033_988_749_895),
    'sqrt2': (0, math.sqrt(2)),
    'catalan': (0, 0.915_965_594_177_219),
    'apery': (0, 1.202_056_903_159_594),
    'khinchin': (0, 2.685_452_001_065_306_2),
    'glaisher': (0, 1.282_427_129_100_622_6),
    'mertens': (0, 0.261_497_212_847_642_77),
    'brun': (0, 1.902_160_583_104),
    'feigenbaumd': (0, 4.669_201_609_102_990_67),
    'feigenbauma': (0, 2.502_907_875_095_892_82),
}

# Based on https://en.wikipedia.org/wiki/List_of_physical_constants
# All quantities in SI units
_PHYSICS_CONSTANTS: FunctionDict = {
    'G': (0, 6.674_30e-11),
    'g': (0, 9.806_65),
    'c': (0, 299_792_458.0),
    'h': (0, 6.626_070_15e-34),
    'hb': (0, 1.054_571_817e-34),
    'mu0': (0, 4 * math.pi * 1e-7),
    'Z0': (0, 376.730_313_668),
    'epsilon0': (0, 8.854_187_812_8e-12),
    'eps0': (0, 8.854_187_812_8e-12),
    'ke': (0, 8.987_551_792_3e9),
    'kB': (0, 1.380_649e-23),
    'sigma': (0, 5.670_374_419e-8),
    'ec': (0, 1.602_176_634e-19),
    'alpha': (0, 7.297_352_569_3e-3),
    'me': (0, 9.109_383_701_5e-31),
    'mp': (0, 1.672_621_923_69e-27),
    'mn': (0, 1.674_927_498_04-27),
    'mmu': (0, 1.883_531_627-28),
    'mtau': (0, 3.167_54e-27),
    'mt': (0, 3.078_4-27),
    'NA': (0, 6.022_140_76e23),
    'R': (0, 8.314_462_618_153_24),
    'dnucs': (0, 9_192_631_770.0)
}


CONSTANTS_FUNCTIONS: FunctionDict = {
    **_MATH_CONSTANTS,
    **_PHYSICS_CONSTANTS,
}
