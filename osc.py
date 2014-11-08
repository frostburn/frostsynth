from math import *

from base import *


def sinehorn_gen(freq, sharpness):
    dt = 2 * pi / get_srate()
    phase = 0.0
    value = 0.0
    for f, s in zip(freq, sharpness):
        s = clip(s, -0.99, 0.99)
        phase += dt * f * (1 + s * value) * (1.0 - s * s) ** -0.5
        value = sin(phase)
        yield value
