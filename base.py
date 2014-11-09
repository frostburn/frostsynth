import math
from itertools import *


_srate = 44100.0


def set_srate(srate=44100.0):
    """Sets the default sampling rate."""
    global _srate
    _srate = srate


def get_srate():
    return _srate


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
        srate = kwargs["srate"]
    else:
        srate = _srate
    
    if len(args)==1:
        start = 0.0
        stop = args[0]
    else:
        start = args[0]
        stop = args[1]

    return islice(source, int(math.floor(srate*start)), int(math.floor(srate*stop)))


def gain(source, g):
    return [s * g for s in source]


def mix(sources, amplitudes=None):
    if amplitudes is None:
        return [sum(samples) for samples in zip(*sources)]
    else:
        return [sum(sample * amplitude for sample, amplitude in zip(samples, amplitudes)) for samples in zip(*sources)]


clip = lambda a, a_min, a_max: a_min if a < a_min else (a_max if a > a_max else a)


epsilon = 1e-10
