from random import *

from base import *


def uniform(duration, vmin=-1.0, vmax=1.0, srate=None):
    """Generate uniform noise in the range from vmin to vmax."""
    if srate is None:
        srate = get_srate()
    if vmin == 0.0 and vmax == 1.0:
        return [random() for _ in range(int(duration * srate))]
    else:
        scale = vmax - vmin
        return [random() * scale + vmin for _ in range(int(duration * srate))]
