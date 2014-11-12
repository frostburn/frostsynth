from random import *

from base import *


def uniform(k, vmin=-1.0, vmax=1.0):
    """Generate uniform noise in the range from vmin to vmax."""
    if vmin == 0.0 and vmax == 1.0:
        return [random() for _ in range(k)]
    else:
        scale = vmax - vmin
        return [random() * scale + vmin for _ in range(k)]


def uniform_t(duration, vmin=-1.0, vmax=1.0, srate=None):
    if srate is None:
        srate = get_srate()
    return uniform(int(duration * srate), vmin=vmin, vmax=vmax)
