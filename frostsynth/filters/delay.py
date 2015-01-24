from math import floor
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


def feedforward_t(source, duration, alpha=1.0, srate=None):
    srate = get_srate(srate)
    return feedforward(source, int(srate * duration), alpha)


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
    srate = get_srate(srate)
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
    srate = get_srate(srate)
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


def thiran_delay2_t(source, duration, fillvalue=0.0, srate=None):
    srate = get_srate(srate)
    return thiran_delay2(source, srate * duration, fillvalue)


def dynamic_delay(source, delta, max_delay=4410):
    """
    Variable length delay.
    No interpolation between samples.
    """
    delta = to_iterable(delta)
    buf = [0] * max_delay
    for sample, d, i in zip(source, delta, cycle(range(max_delay))):
        buf[i] = sample
        yield buf[i - int(floor(d))]

def dynamic_delay1(source, delta, max_delay=4410):
    """
    First order Lagrange delay.
    Linear interpolation between samples.
    """
    delta = to_iterable(delta)
    max_delay += 1
    buf = [0] * max_delay
    for sample, d, i in zip(source, delta, cycle(range(max_delay))):
        buf[i] = sample
        int_d = int(floor(d))
        d = d - int_d
        x1 = buf[i - int_d - 1]
        x0 = buf[i - int_d]
        yield x0 + d * (x1 - x0)

#TODO: make non-causal to allow delays < 1 sample?
def dynamic_delay3(source, delta, max_delay=4410):
    """Third order Lagrange delay."""
    delta = to_iterable(delta)
    max_delay += 3
    buf = [0] * max_delay
    for sample, d, i in zip(source, delta, cycle(range(max_delay))):
        buf[i] = sample
        int_d = int(floor(d - 1))
        d = d - int_d
        x3 = buf[i - int_d - 3]
        x2 = buf[i - int_d - 2]
        x1 = buf[i - int_d - 1]
        x0 = buf[i - int_d]

        # TODO: Factor out to minimize the number of multiplications.
        yield x0 + d * (-11 * x0 + 18 * x1 - 9 * x2 + 2 * x3 + d * (6 * x0 - 15 * x1 + 12 * x2 - 3 * x3 + d * (-x0 + 3 * x1 - 3 * x2 + x3))) * 0.1666666666666666666666666
