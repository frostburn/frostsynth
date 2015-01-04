import math
from itertools import *
from collections import Iterable, Sequence


_srate = 44100.0


def set_srate(srate=44100.0):
    """Sets the default sampling rate."""
    global _srate
    _srate = srate
    return _srate


def get_srate(default=None):
    """Gets the default sampling rate."""
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


def constant(value, k):
    return [value] * k


def constant_t(value, duration, srate=None):
    if srate is None:
        srate = _srate
    return constant(value=value, k=int(duration * srate))


def impulse(k, value=1.0):
    return [value] + [0.0] * (k - 1)


def impulse_t(duration, value=1.0, srate=None):
    if srate is None:
        srate = _srate
    return impulse(int(duration * srate), value=value)


def linspace(start, end, samples):
    scale = (end - start) / (samples - 1)
    return [start + i * scale for i in range(samples)]


def linspace_t(start, end, duration, srate=None):
    if srate is None:
        srate = _srate
    return linspace(start, end, int(duration * srate))


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


def timed(*iterables, t0=0.0, srate=None):
    return zip(*((time_gen(t0, srate),) + iterables))


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


def timeslice_gen(source, *args, **kwargs):
    """timeslice_gen(iterable[,start], stop, srate=None) --> elements of iterable between times start and stop."""
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


def timeslice(source, *args, **kwargs):
    if isinstance(source, Sequence):
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

        return source[int(srate * start):int(srate * stop)]
    else:
        return list(timeslice_gen(source, *args, **kwargs))


def warmup_gen(source, t0, srate=None):
    if srate is None:
        srate = _srate
    k = int(t0 * srate)
    source = iter(source)
    for i in range(k):
        next(source)
    return source


def gain(source, g):
    return [s * g for s in source]


def gain_gen(source, g):
    return (s * g for s in source)


def ringm(source0, source1):
    return [s0 * s1 for s0, s1 in zip(source0, source1)]


def ringm_gen(source0, source1):
    return (s0 * s1 for s0, s1 in zip(source0, source1))


def add(*args):
    return [sum(samples) for samples in zip(*args)]


def add_gen(*args):
    return map(sum, zip(*args))


def mix(sources, amplitudes=None):
    if amplitudes is None:
        return [sum(samples) for samples in zip(*sources)]
    else:
        return [sum(sample * amplitude for sample, amplitude in zip(samples, amplitudes)) for samples in zip(*sources)]


# TODO: Amplitudes
def mix_gen(sources):
    return map(sum, zip(*sources))


def mix_longest_gen(sources):
    sources = [iter(source) for source in sources]
    while True:
        result = 0
        for source in sources[:]:
            try:
                result += next(source)
            except StopIteration:
                sources.remove(source)
        if not sources:
            return
        yield result


def mix_longest(sources):
    return list(mix_longest_gen(sources))


def to_iterable(source):
    if isinstance(source, Iterable):
        return iter(source)
    else:
        return repeat(source)


def to_sequence(source, n):
    if isinstance(source, Sequence):
        return source
    else:
        return [source] * n


class Infinitee(object):
    def __init__(self, generator):
        self.generator = generator

    def __iter__(self):
        self.generator, t = tee(self.generator)
        return t


class RandomAccessIterator(object):
    def __init__(self, iterator):
        self._iterator = iter(iterator)
        self._values = []

    def __getitem__(self, key):
        if key < 0:
            raise ValueError("Negative indexing not supported.")
        while len(self._values) <= key:
            self._values.append(next(self._iterator))
        return self._values[key]


def interlace(*iterables):
    iterables = [iter(it) for it in iterables]
    while True:
        for it in iterables:
            yield next(it)


def pan(source, panning=0.5):
    return gain(source, 2 * (1 - panning) if panning > 0.5 else 1), gain(source, 2 * panning if panning < 0.5 else 1)

def stereo_mix(sources, amplitudes=None):
    lefts, rights = zip(*sources)
    return mix(lefts, amplitudes), mix(rights, amplitudes)


clip = lambda a, a_min, a_max: a_min if a < a_min else (a_max if a > a_max else a)


epsilon = 1e-10


def equal(a, b):
    return abs(a - b) <= epsilon


two_pi = 2 * math.pi


two_pi_j = two_pi * 1j


pi_squared = math.pi * math.pi

i_pi = 1 / math.pi


i_two_pi = 1 / two_pi


e = math.exp(1)
