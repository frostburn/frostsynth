from math import *
from itertools import *

from base import *


two_pi = 2 * pi


def sineping_gen(amplitude, frequency, decay, theta=0, srate=None):
    """Generates amplitude * sin(2 * pi * t * frequency + theta) * exp(-t * decay)."""
    if srate is None:
        srate = get_srate()

    dt = 1.0 / srate


    d = exp(-dt * decay)
    i_d = 1.0 / d
    w = two_pi * dt * frequency

    a1 = -2 * d * cos(w)
    a2 = d * d

    y1 = amplitude * sin(theta - w - w) * i_d * i_d
    y0 = amplitude * sin(theta - w ) * i_d

    a1 = -a1
    while True:
        y2 = y0
        y0 = a1 * y0 - a2 * y1
        yield y0
        y1 = y0
        y0 = a1 * y0 - a2 * y2
        yield y0


def sinepings_gen(amplitudes, frequencies, decays, thetas=None, srate=None):
    if thetas is None:
        thetas = repeat(0)
    sps = [sineping_gen(*params) for params in zip(amplitudes, frequencies, decays, thetas, repeat(srate))]
    return mix_gen(sps)
