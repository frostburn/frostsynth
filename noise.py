from random import *

from base import *


_x = randint(0, 2147483647)


def fast_uniform(duration, vmin=-1.0, vmax=1.0, srate=None):
    if srate is None:
        srate = get_srate()
    k = int(duration * srate)
    buf = [0.0] * k
    scale = (vmax - vmin) / 2147483647
    global _x
    for i in range(k):
        _x = (_x * 1103515245 + 12345) & 2147483647
        buf[i] = _x * scale + vmin
    return buf


def uniform(duration, vmin=-1.0, vmax=1.0, srate=None):
    """Generate uniform noise in the range from vmin to vmax."""
    if srate is None:
        srate = get_srate()
    if vmin == 0.0 and vmax == 1.0:
        return [random() for _ in range(int(duration * srate))]
    else:
        scale = vmax - vmin
        return [random() * scale + vmin for _ in range(int(duration * srate))]
