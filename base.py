import math
from itertools import *


_srate = 44100.0


def set_srate(srate=44100.0):
    """Sets the default sampling rate."""
    global _srate
    _srate = srate
    return _srate


def get_srate(default=None):
    if default is None:
        return _srate
    else:
        return default


class Srate(object):
    def __init__(self, srate):
        self.srate = srate

    def __enter__(self):
        global _srate
        self.old_srate = _srate
        _srate = self.srate

    def __exit__(self, *args, **kwargs):
        global _srate
        _srate = self.old_srate


def zero(k):
    return [0.0] * k


def zero_t(duration, srate=None):
    if srate is None:
        srate = _srate
    return zero(int(duration * srate))

def range_t(*args, step=None, srate=None):
    if srate is None:
        srate = _srate
    if len(args) == 1:
        stop = int(args[0] * srate)
        return range(stop)
    elif len(args) == 2:
        start = int(args[0] * srate)
        stop = int(args[1] * srate)
        if step is None:
            step = 1
        else:
            step = int(step * srate)
        return range(start, stop, step)


def time_k(k, t0=0.0, srate=None):
    if srate is None:
        srate = _srate
    dt = 1.0 / srate
    return [t0 + i * dt for i in range(k)]


def time(duration, t0=0.0, srate=None):
    if srate is None:
        srate = _srate
    dt = 1.0 / srate
    return [t0 + i * dt for i in range(int(duration * srate))]


def time_gen(t0=0.0, srate=None):
    """Generates successive instants of time starting at t0."""
    if srate is None:
        srate = _srate
    dt = 1.0 / srate
    return (t0 + i * dt for i in count())


def time_dt_gen(dt, t0=0.0):
    return (t0 + i * dt for i in count())


def differentiate_gen(source, srate=None):
    if srate is None:
        srate = _srate
    source0, source1 = tee(source)
    next(source1)
    return ((s1 - s0) * srate for s0, s1 in zip(source0, source1))


def differentiate(source, srate=None):
    if srate is None:
        srate = _srate
    return [(s1 - s0) * srate for s0, s1 in zip(source, source[1:])]


def integrate_gen(source, srate=None):
    """
    Integrates 'source' with respect to time.
    For example if source is frequency then integrate() yields phase.
    """
    if srate is None:
        srate = _srate
    dt = 1.0 / srate
    return accumulate(s * dt for s in source)


def integrate(source, srate=None):
    return list(integrate_gen(source, srate))


def timeslice(source, *args, **kwargs):
    """timeslice(iterable[,start], stop, srate=None) --> elements of iterable between times start and stop."""
    if "srate" in kwargs:
        srate = get_srate(kwargs["srate"])
    else:
        srate = _srate
    
    if len(args)==1:
        start = 0.0
        stop = args[0]
    else:
        start = args[0]
        stop = args[1]

    return islice(source, int(srate * start), int(srate * stop))


def gain(source, g):
    return [s * g for s in source]


def gain_gen(source, g):
    return (s * g for s in source)


def ringm(source0, source1):
    return [s0 * s1 for s0, s1 in zip(source0, source1)]


def ringm_gen(source0, source1):
    return (s0 * s1 for s0, s1 in zip(source0, source1))


def mix(sources, amplitudes=None):
    if amplitudes is None:
        return [sum(samples) for samples in zip(*sources)]
    else:
        return [sum(sample * amplitude for sample, amplitude in zip(samples, amplitudes)) for samples in zip(*sources)]


def mix_gen(sources):
    return map(sum, zip(*sources))


clip = lambda a, a_min, a_max: a_min if a < a_min else (a_max if a > a_max else a)


epsilon = 1e-10


two_pi = 2.0 * math.pi


two_pi_j = two_pi * 1j


i_pi = 1.0 / math.pi
