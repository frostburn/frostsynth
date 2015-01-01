from math import *

from frostsynth import *


def decay_envelope_gen(amplitude, decay, srate=None):
    """
    Generates amplitude * exp(-t * decay)
    """
    srate = get_srate(srate)
    d = exp(-decay / srate)
    y = amplitude
    while True:
        yield y
        y *= d


def decay_env_gen(source, amplitude, decay, srate=None):
    envelope = decay_envelope_gen(amplitude, decay, srate)
    return (s * e for s, e in zip(source, envelope))


def decay_env(source, amplitude, decay, srate=None):
    envelope = decay_envelope_gen(amplitude, decay, srate)
    return [s * e for s, e in zip(source, envelope)]


def decay2_envelope_gen(amplitude, t_max, decay=None, srate=None):
    """
    Generates amplitude * t * exp(1-t) scaled so that the maximum amplitude is reached at time t_max.
    If decay is set decays approximately as exp(-t * decay) after that.
    """
    srate = get_srate(srate)
    dt = 1 / (srate * t_max)
    d0 = exp(-dt)
    d1 = dt * exp(-2 * dt)
    y_0 = amplitude * e
    y_1 = 0
    if decay is not None:
        while y_0 > 1:
            y_1 = d0 * y_1 + d1 * y_0
            y_0 *= d0
            yield y_1
        dt = decay / srate
        d0 = exp(-dt)
        d1 = dt * exp(-2 * dt)
    while True:
        y_1 = d0 * y_1 + d1 * y_0
        y_0 *= d0
        yield y_1


def decay2_env_gen(source, amplitude, t_max, decay=None, srate=None):
    envelope = decay2_envelope_gen(amplitude, t_max, decay, srate)
    return (s * e for s, e in zip(source, envelope))


def decay2_env(source, amplitude, t_max, decay=None, srate=None):
    envelope = decay2_envelope_gen(amplitude, t_max, decay, srate)
    return [s * e for s, e in zip(source, envelope)]


def hold_release_env(source, hold, release, full=False, srate=None):
    srate = get_srate(srate)
    buf = timeslice(source, hold + release, srate=srate)
    k = int(srate * hold)
    if release == 0.0:
        return buf
    i_k_release = 1.0 / (srate * release)
    for i in range(k, len(buf)):
        buf[i] *= 1.0 - (i - k) * i_k_release
    if full:
        return buf + [0.0] * (len(list(source)) - len(buf))
    else:
        return buf
