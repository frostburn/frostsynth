from itertools import *

from frostsynth import *
from frostsynth.filters.base import *


def delay(iterable, k, fillvalue=0.0):
    """Delays the evaluation of iterable by k steps."""
    return chain(repeat(fillvalue,k), iterable)


def delay_t(iterable, duration, fillvalue=0.0, srate=None):
    """Delays the evaluation of iterable by 'duration'."""
    if srate is None:
        srate = get_srate()
    return delay(iterable, int(srate * duration), fillvalue)


def feedforward(source, k, alpha=1.0):
    """Feedforward comb filter: y[n] = x[n] + alpha x[n-k]."""
    if k < 1:
        raise ValueError("Minimum delay is one sample.")
    buf = [0.0] * k
    i = 0
    for sample in source:
        yield sample + alpha * buf[i]
        buf[i] = sample
        i += 1
        if i == k:
            i = 0


def comb(source, k, alpha=1.0):
    """Feedback comb filter: y[n] = x[n] + alpha y[n-k]."""
    if k < 1:
        raise ValueError("Minimum delay is one sample.")
    buf = [0.0] * k
    i = 0
    for sample in source:
        buf[i] = buf[i] * alpha + sample
        yield buf[i]
        i += 1
        if i == k:
            i = 0


def comb_t(source, duration, alpha=1.0, srate=None):
    if srate is None:
        srate = get_srate()
    return comb(source, int(srate * duration), alpha)


feedback = comb
feedback_t = comb_t


def filtered_comb(source, k, filter):
    if k < 1:
        raise ValueError("Minimum delay is one sample.")

    def output():
        for sample, d in zip(source, delayed_filtered_output):
            yield sample + d

    output, output_ = tee(output())

    delayed_filtered_output = delay(filter(output_), k)

    return output


def filtered_comb_t(source, duration, filter, srate=None):
    if srate is None:
        srate = get_srate()
    return filtered_comb(source, int(srate * duration), filter)


def schroeder(source, k, g=1.0):
    """Schroeder all pass filter: y[n] + g y[n-k] = g.conjugate() x[n] + x[n-k]."""
    if k < 1:
        raise ValueError("Minimum delay is one sample.")
    buf = [0.0] * k
    i = 0
    gc = g.conjugate()
    for sample in source:
        temp = sample - g * buf[i]
        yield gc * temp + buf[i]
        buf[i] = temp
        i += 1
        if i == k:
            i = 0


def schroeder_t(source, duration, g=1.0, srate=None):
    if srate is None:
        srate = get_srate()
    return schroeder(source, int(srate * duration), g)


def thiran_delay1(source, delta, fillvalue=0.0):
    """First order Thiran allpass delay."""
    k = int(floor(delta - 0.5))
    d = delta - k
    a0 = 1.0
    a1 = -d / (1.0 + d)
    return delay(polezero(source, a0, a1, a1, a0), k, fillvalue)


def thiran_delay2(source, delta, fillvalue=0.0):
    """Second order Thiran allpass delay."""
    k = int(floor(delta - 1.5))
    d = delta - k
    a0 = 1.0
    a1 = 4.0 / (1.0 + d) - 2.0
    a2 = d * (d - 1.0) / (2.0 + d * (3.0 + d))
    return delay(biquad(source, a0, a1, a2, a2, a1, a0), k, fillvalue)