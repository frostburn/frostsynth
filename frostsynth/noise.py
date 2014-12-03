from random import *
from cmath import rect as from_polar
from math import sqrt

from frostsynth import *
from frostsynth.interpolation import *
from frostsynth.ffi import uniform as fast_uniform


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
        return from_polar(1, two_pi * random())
    else:
        return [from_polar(1, two_pi * random()) for _ in range(k)]


def cunit_t(duration, srate=None):
    srate = get_srate(srate)
    return cunit(int(duration * srate))


def pink_gen(octaves=16):
    """
    Generates a sum of successive octaves of white noise to create approximate pink noise.

    Normalized to have unit variance.
    """
    shift = -0.5 * octaves
    scale = sqrt(12.0 / octaves)
    values = [random() for _ in range(octaves)]
    for i in count():
        # Each value is updated in the middle of every 2 ** k:th step.
        values[0] = random()
        for j  in range(octaves - 1):
            if i & ((1 << (j + 1)) - 1) == 1 << j:
                values[j + 1] = random()
        yield (sum(values) + shift) * scale


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

        frequency = to_iterable(frequency)

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


def lpnoise_gen(bandwidth, order=2, srate=None):
    srate = get_srate(srate)
    bw = two_pi * bandwidth / srate
    bw2 = bw * bw
    d = 1 + (order * bw2 - bw * sqrt((4 + order * bw2) * order)) * 0.5
    d1 = 1 - d
    two_sqrt_d1 = 2 * sqrt(d1)
    y = [0.0] * order
    while  True:
        y[0] = two_sqrt_d1 * (random() - 0.5) + d * y[0]
        for i in range(order - 1):
            y[i + 1] = d1 * y[i] + d * y[i + 1]
        yield y[-1]


def dynamic_lpnoise_gen(bandwidth, order=2, srate=None):
    srate = get_srate(srate)
    m = two_pi / srate
    y = [0.0] * order
    for b in bandwidth:
        bw = m * b
        bw2 = bw * bw
        d = 1 + (order * bw2 - bw * sqrt((4 + order * bw2) * order)) * 0.5
        d1 = 1 - d
        y[0] = 2 * sqrt(d1) * (random() - 0.5) + d * y[0]
        for i in range(order - 1):
            y[i + 1] = d1 * y[i] + d * y[i + 1]
        yield y[-1]
