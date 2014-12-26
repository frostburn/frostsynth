from __future__ import division
from math import pi, exp, cosh, cos, log, floor
from cmath import rect as from_polar, exp as cexp


__author__ = "Lumi Pakkanen"
__copyright__ = "Copyright 2014, Lumi Pakkanen"
__credits__ = ["Lumi Pakkanen"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Lumi Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "Initial release"


__all__ = [
    "theta", "formant", "theta_formant"
]


epsilon = 1e-10


two_pi = 2 * pi
pi_squared = pi * pi
half_pi_squared = 0.5 * pi * pi


def theta(t, q):
    """Peak-amplitude normalized Jacobi theta(t, q)."""
    if q < epsilon:
        q = epsilon
    if q < 0.2:
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9

        c = cos(two_pi * t)
        c2 = 2 * c * c - 1
        c3 = 2 * c * c2 - c
        c4 = 2 * c * c3 - c2
        c5 = 2 * c * c4 - c3

        return (1.0 + 2 * (q * c + q4 * c2 + q9 * c3 + q16 * c4 + q25 * c5)) / (1.0 + 2 * (q + q4 + q9 + q16 + q25))
    elif q < 0.9:
        t -= floor(t + 0.5)
        a = pi_squared / log(q)
        m = exp(-a * 2 * t)
        b = exp(a)
        b4 = b ** 4

        z2 = m * m
        z3 = m * z2
        z4 = m * z3
        s = z2 + b * (m + z3) + b4 * (1 + z4)

        return exp(a * t * (t + 4)) * s / (1 + 2 * (b + b4))
    elif q < 1:
        t -= floor(t + 0.5)
        a = pi_squared / log(q)
        return exp(a * t * t)
    else:
        return 0.0


def formant(phase, ratio, width):
    """Formant waveform with energy concentrated on the harmonic specified by ratio."""
    ratio = floor(ratio)
    if width < 700:
        x = pi * phase
        return cosh(cos(x) * width) / cosh(width) * cos(2 * x * ratio)
    else:
        x = phase - floor(phase + 0.5)
        return exp(-half_pi_squared * width * x * x) * cos(two_pi * x * ratio)


def theta_formant(phase, ratio, width):
    """Formant waveform with energy concentrated on the fractional harmonic specified by ratio."""
    if width < epsilon:
        width = epsilon
    if width < 7:
        x = two_pi * phase
        q = exp(-pi_squared / width)
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9
        norm = 1 + 2 * (q + q4 + q9 + q25)
        floor_ratio = floor(ratio)
        ratio -= floor_ratio
        cn = cos(x * (floor_ratio - 5))
        cn1 = cos(x * (floor_ratio - 4))
        c = cos(x)
        s = cn1 * q ** (4 + ratio) ** 2
        for n in range(-3, 5):
            cn1, cn = 2 * c * cn1 - cn, cn1
            s += cn1 * q ** (n - ratio) ** 2
        return s / norm
    elif width < 100:
        x = phase - floor(phase + 0.5)
        ratio *= two_pi
        z = from_polar(1, ratio * (x + 2))
        m = cexp(2 * width * x - 1j * ratio)
        b = exp(-width)
        b4 = b ** 4

        z0 = z.real
        z *= m
        z1 = z.real
        z *= m
        s = z.real
        z *= m
        s += (z.real + z1) * b
        z *= m
        s += (z.real + z0) * b4

        return exp(-width * x * (x + 4)) * s / (1 + 2 * (b + b4))
    else:
        x = phase - floor(phase + 0.5)
        return exp(-width * x * x) * cos(two_pi * x * ratio)
