from __future__ import division
from math import pi, floor, sin, cos, atan2


__author__ = "Lumi Pakkanen"
__copyright__ = "Copyright 2014, Lumi Pakkanen"
__credits__ = ["Lumi Pakkanen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Lumi Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "Initial release"


__all__ = [
    "lissajous11", "lissajous12", "lissajous13", "lissajous14", "lissajous15",
    "lissajous23", "lissajous25", "lissajous34", "lissajous35", "lissajous45", "lissajous56"
]

clip = lambda a, a_min, a_max: a_min if a < a_min else (a_max if a > a_max else a)


epsilon = 1e-10


one_per_pi = 1 / pi
two_per_pi = 2 / pi
four_thirds_per_pi = 4 / (3 * pi)
four_fifths_per_pi = 4 / (5 * pi)
four_sevenths_per_pi = 4 / (7 * pi)
four_ninths_per_pi = 4 / (9 * pi)
four_elevenths_per_pi = 4 / (11 * pi)
pi_per_twelve = pi / 12
pi_per_ten = pi / 10
pi_per_eight = pi / 8
pi_per_six = pi / 6
half_pi = 0.5 * pi
two_pi = 2 * pi
three_pi = 3 * pi
four_pi = 4 * pi
five_pi = 5 * pi
six_pi = 6 * pi
eight_pi = 8 * pi
ten_pi = 10 * pi
twelve_pi = 12 * pi


def lissajous11(phase, sharpness=0):
    if abs(sharpness) < epsilon:
        return sin(two_pi * phase)
    x = pi * (phase - floor(phase + 0.5))
    s = clip(sharpness, epsilon - 1, 1 - epsilon)
    a = 1 + s
    b = 1 - s
    return (atan2(a * a * sin(x), b * b * cos(x)) - x) / (2 * atan2(b, a) - half_pi)


def lissajous12(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = half_pi * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(two_pi * phase), (1 - s) * cos(four_pi * phase + b)) * four_thirds_per_pi


def lissajous13(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(three_pi * x), (1 - s) * cos(pi * x + b)) * two_per_pi + x + x


def lissajous14(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = pi_per_eight * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 - s) * cos(two_pi * phase + b), (1 + s) * cos(eight_pi * phase)) * 0.39328116619206743


def lissajous15(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(pi * x + b)) * 0.4754858297894094 - 1.4937827897524554 * x


def lissajous16(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = half_pi * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 - s) * sin(two_pi * phase), (1 + s) * cos(twelve_pi * phase + b)) * 0.3708887239244341


def lissajous23(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(six_pi * x), (1 - s) * cos(four_pi * x + b))
    if x > 0 and l < 0:
        l += two_pi
    elif x < 0 and l > 0:
        l -= two_pi
    return l * four_fifths_per_pi


def lissajous25(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((-1 - s) * sin(ten_pi * x), (1 - s) * cos(four_pi * x + b))
    if 0.15 < x < 0.35 and l < 0:
        l += two_pi
    elif -0.35 < x < -0.15 and l > 0:
        l -= two_pi
    return l * four_fifths_per_pi


def lissajous34(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 - s) * sin(six_pi * x), (1 + s) * cos(eight_pi * x + b))
    if 0.1 < x < 0.4 and l < 0:
        l += two_pi
    elif -0.4 < x < -0.1 and l > 0:
        l -= two_pi
    return l * four_sevenths_per_pi


def lissajous35(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(three_pi * x + b))
    if x > 0 and l < 0:
        l += two_pi
    elif x < 0 and l > 0:
        l -= two_pi
    return l * one_per_pi - x


def lissajous45(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(ten_pi * x), (1 - s) * cos(eight_pi * x + b))
    if (x > 0 and l < 0) or (0.15 < x < 0.35):
        l += two_pi
    elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
        l -= two_pi
    return l * four_ninths_per_pi


def lissajous56(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 - s) * sin(ten_pi * x), (1 + s) * cos(twelve_pi * x + b))
    if (x > 0 and l < 0) or (0.15 < x < 0.35):
        l += two_pi
    elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
        l -= two_pi
    return l * four_elevenths_per_pi
