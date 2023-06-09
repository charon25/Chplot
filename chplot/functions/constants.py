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
    'nan': (0, math.nan),
    '_': (0, math.nan),
    'inf': (0, math.inf),
}

# Based on https://en.wikipedia.org/wiki/List_of_physical_constants
# All quantities in SI units
_PHYSICS_CONSTANTS: FunctionDict = {
    'G': (0, 6.674_3e-11),
    'g': (0, 9.806_65),
    'c': (0, 299_792_458.0),
    'h': (0, 6.626_070_15e-34),
    'hb': (0, 1.054_571_817e-34),
    'mu0': (0, 1.256_637_602_12e-6),
    'Z0': (0, 376.730_313_668),
    'epsilon0': (0, 8.854_187_812_8e-12),
    'eps0': (0, 8.854_187_812_8e-12),
    'ke': (0, 8.987_551_792_3e9),
    'kB': (0, 1.380_649e-23),
    'sigma': (0, 5.670_374_419e-8),
    'c1': (0, 3.741_771_852e-16),
    'c1L': (0, 1.191_042_972_397_188e-16),
    'c2': (0, 1.438_776_877e-2),
    'b': (0, 2.897_771_955e-3),
    'bp': (0, 5.878_925_757e10),
    'bent': (0, 3.002_916_077e-3),
    'ec': (0, 1.602_176_634e-19),
    'G0': (0, 7.748091729e-5),
    'RK': (0, 25_812.807_45),
    'KJ': (0, 483_597.848_4e9),
    'alpha': (0, 7.297_352_569_3e-3),
    'me': (0, 9.109_383_701_5e-31),
    'mp': (0, 1.672_621_923_69e-27),
    'mn': (0, 1.674_927_498_04-27),
    'mmu': (0, 1.883_531_627-28),
    'mtau': (0, 3.167_54e-27),
    'mt': (0, 3.078_4-27),
    'ge': (0, -2.002_319_304_362_56),
    'gmu': (0, -2.002_331_841_8),
    'gP': (0, 5.585_694_689_3),
    'muB': (0, 9.274_010_078_3e-24),
    'muN': (0, 5.050_783_746_1e-27),
    're': (0, 2.817_940_326_2e-15),
    'sigmae': (0, 6.652_458_732_1e-29),
    'a0': (0, 5.291_772_109_03e-11),
    'Eh': (0, 4.359_744_722_207_1e-18),
    'Ry': (0, 2.179_872_361_103_5e-18),
    'Rinf': (0, 1.097_373_156_816e7),
    'GF0': (0, 4.5437957e14),
    'F': (0, 9.648_533_212_331_002e4),
    'm12C': (0, 1.992_646_879_92e-26),
    'M12C': (0, 11.999_999_995_8e-3),
    'mu': (0, 1.660_539_066_6e-27),
    'Mu': (0, 0.999_999_999_65e-3),
    'VmSi': (0, 1.205_883_199e-5),
    'NA': (0, 6.022_140_76e23),
    'R': (0, 8.314_462_618_153_24),
    'dnuCs': (0, 9_192_631_770.0),

    'eV': (0, 1.602_176_634e-19),
}


# Planets data source: https://nssdc.gsfc.nasa.gov
_ASTRONOMY_CONSTANTS: FunctionDict = {
    'Msun': (0, 1.988_5e30),
    'Rsun': (0, 6.957e8),
    'Mmercury': (0, 3.301e23),
    'Rmercury': (0, 2.439_7e6),
    'Mvenus': (0, 4.867_3e24),
    'Rvenus': (0, 6.051_8e6),
    'Mearth': (0, 5.972_2e24),
    'Rearth': (0, 6.371e6),
    'Mmoon': (0, 7.346e22),
    'Rmoon': (0, 1.737_4e6),
    'Mmars': (0, 6.416_9e23),
    'Rmars': (0, 3.389_5e6),
    'Mjupiter': (0, 1.898_13e27),
    'Rjupiter': (0, 6.991_1e7),
    'Msaturn': (0, 5.683_2e26),
    'Rsaturn': (0, 5.8232e7),
    'Muranus': (0, 8.681_1e25),
    'Ruranus': (0, 2.536_2e7),
    'Mneptune': (0, 1.024_09e26),
    'Rneptune': (0, 2.462_2e7),
    'Mpluto': (0, 1.303e22),
    'Rpluto': (0, 1.188e6),
    'Mcharon': (0, 1.586e21),
    'Rcharon': (0, 6.06e5),

    'AU': (0, 1.495_978_707e11),
    'ly': (0, 9.460_730_472_580_8e15),
    'pc': (0, 3.085_677_581_491_367_3e16),
}


CONSTANTS_FUNCTIONS: FunctionDict = {
    **_MATH_CONSTANTS,
    **_PHYSICS_CONSTANTS,
    **_ASTRONOMY_CONSTANTS,
}
