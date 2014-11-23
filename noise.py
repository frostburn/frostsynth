from random import *
from cmath import rect

from base import *
from interpolation import *
from ffi import uniform as fast_uniform


def fast_uniform_t(duration, srate=None):
    srate = get_srate(srate)
    return fast_uniform(int(duration * srate))


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
    srate = get_srate(srate)
    return uniform(int(duration * srate), vmin=vmin, vmax=vmax)


def cunit(k=None):
    if k is None:
        return rect(1, two_pi * random())
    else:
        return [rect(1, two_pi * random()) for _ in range(k)]


def cunit_t(duration, srate=None):
    srate = get_srate(srate)
    return cunit(int(duration * srate))


def snow0_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    """Constant interpolated white noise from vmin to vmax driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1.0 / srate
    frequency = iter(frequency)

    target = 1.0
    phase = target
    while True:
        if phase >= target:
            y0 = uniform(vmin=vmin, vmax=vmax)
            phase = phase % target
            target = 1.0 + (random() - 0.5) * variability
        yield y0
        phase += dt * next(frequency)


def snow1_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    """Linear interpolated white noise from vmin to vmax driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1.0 / srate
    frequency = iter(frequency)

    y1 = uniform(vmin=vmin, vmax=vmax)
    target = 1.0
    phase = target
    while True:
        if phase >= target:
            y0 = y1
            y1 = uniform(vmin=vmin, vmax=vmax)
            phase = phase % target
            target = 1.0 + (random() - 0.5) * variability
            i_target = 1.0 / target
        yield y0 + (y1 - y0) * phase * i_target
        phase += dt * next(frequency)


def _func_snow3_gen(func):
    def snow3_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
        """
        Cubic interpolated noise controlled by 'frequency'.

        Approximately withing range from vmin to vmax, but does overshoot.
        """
        srate = get_srate(srate)
        dt = 1.0 / srate
        frequency = iter(frequency)

        y3 = uniform(vmin=vmin, vmax=vmax)
        y2 = uniform(vmin=vmin, vmax=vmax)
        y1 = uniform(vmin=vmin, vmax=vmax)
        target = 1.0
        phase = target
        while True:
            if phase >= target:
                y0 = y1
                y1 = y2
                y2 = y3
                y3 = uniform(vmin=vmin, vmax=vmax)
                phase = phase % target
                target = 1.0 + (random() - 0.5) * variability
                i_target = 1.0 / target
            yield func(phase * i_target, y0, y1, y2, y3)
            phase += dt * next(frequency)

    return snow3_gen

snow3_gen = _func_snow3_gen(lagrange_four_point)

spline_snow_gen = _func_snow3_gen(catmull_rom_spline)
