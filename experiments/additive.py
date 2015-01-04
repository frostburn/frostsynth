from __future__ import division
from math import pi, exp, sin, cos
from cmath import rect as from_polar


__author__ = "Lumi Pakkanen"
__copyright__ = "Copyright 2015, Lumi Pakkanen"
__credits__ = ["Lumi Pakkanen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Lumi Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "Initial release"


__all__ = [
    "sineping_gen",
    "cos_sum", "cos_octave_sum",
    "sin_sum", "sin_odd_sum", "sin_octave_sum", "sin_tritave_sum",
    "cis_sum"
]


two_pi = 2 * pi
four_pi = 4 * pi


def sineping_gen(amplitude, frequency, decay, phi=0, srate=44100):
    """Generates amplitude * sin(2 * pi * t * frequency + phi) * exp(-t * decay)."""
    dt = 1 / srate

    d = exp(-dt * decay)
    w = two_pi * dt * frequency

    a1 = 2 * d * cos(w)
    a2 = d * d

    y1 = amplitude * sin(phi)
    yield y1

    y0 = amplitude * sin(phi + w) * d
    yield y0

    while True:
        y2 = y0
        y0 = a1 * y0 - a2 * y1
        yield y0
        y1 = y0
        y0 = a1 * y0 - a2 * y2
        yield y0


def cos_sum(phase, coefs):
    """Evaluates sum(coef * cos(2 * pi * k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0]
    elif len(coefs) == 2:
        return coefs[0] + coefs[1] * cos(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        c2 = c + c
        bk = coefs[-1]
        bk1 = coefs[-2] + c2 * bk
        for coef in coefs[-3:0:-1]:
            bk1, bk = coef + c2 * bk1 - bk, bk1
        return coefs[0] + c * bk1 - bk


def cos_octave_sum(phase, coefs):
    """Evaluates sum(coef * cos(2 * pi * 2 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * cos(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        result = coefs[0] * c
        for coef in coefs[1:]:
            c = 2 * c * c - 1
            result += coef * c
        return result


def sin_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * k * phase) for k, coef in enumerate(coefs, 1))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    elif len(coefs) == 2:
        return coefs[0] * sin(two_pi * phase) + coefs[1] * sin(four_pi * phase)
    else:
        c2 = 2 * cos(two_pi * phase)
        bk = coefs[-1]
        bk1 = coefs[-2] + c2 * bk
        for coef in coefs[-3:0:-1]:
            bk1, bk = coef + c2 * bk1 - bk, bk1
        return sin(two_pi * phase) * (coefs[0] + c2 * bk1 - bk)


def sin_odd_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * (2 * k - 1) * phase) for k, coef in enumerate(coefs, 1))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        s = sin(two_pi * phase)
        s2 = 2 - 4 * s * s
        bk = coefs[-1]
        bk1 = coefs[-2] + s2 * bk
        for coef in coefs[-3::-1]:
            bk1, bk = coef + s2 * bk1 - bk, bk1
        return s * (bk1 + bk)


def sin_octave_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * 2 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        s = sin(two_pi * phase)
        result = coefs[0] * s
        s *= c + c
        result += coefs[1] * s
        for coef in coefs[2:]:
            c = 2 * c * c - 1
            s *= c + c
            result += coef * s
        return result


def sin_tritave_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * 3 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        s = sin(two_pi * phase)
        result = coefs[0] * s
        for coef in coefs[1:]:
            s = s * (3 - 4 * s * s)
            result += coef * s
        return result


def cis_sum(phase, coefs, sharpness=1):
    """Evaluates sum(coef * sharpness ** k * exp(2j * pi * k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0j
    else:
        z = from_polar(sharpness, two_pi * phase)
        result = coefs[-1]
        for coef in coefs[-2::-1]:
            result = coef + z * result
        return result
