from random import *
from cmath import rect

from base import *


def uniform(k=None, vmin=-1.0, vmax=1.0):
    """Generate uniform noise in the range from vmin to vmax."""
    if vmin == 0.0 and vmax == 1.0:
        if k is None:
            return random()
        else:
            return [random() for _ in range(k)]
    else:
        scale = vmax - vmin
        if k is None:
            return random() * scale + vmin
        else:
            return [random() * scale + vmin for _ in range(k)]


def uniform_t(duration, vmin=-1.0, vmax=1.0, srate=None):
    if srate is None:
        srate = get_srate()
    return uniform(int(duration * srate), vmin=vmin, vmax=vmax)


def cunit():
    return rect(1, two_pi * random())
