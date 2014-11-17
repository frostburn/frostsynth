from math import *
from itertools import *

from base import *


def sineping_gen(amplitude, frequency, decay, theta=0, srate=None):
    """Generates amplitude * sin(2 * pi * t * frequency + theta) * exp(-t * decay)."""
    if srate is None:
        srate = get_srate()

    dt = 1.0 / srate


    d = exp(-dt * decay)
    i_d = 1.0 / d
    w = two_pi * dt * frequency

    a1 = 2 * d * cos(w)
    a2 = d * d

    y1 = amplitude * sin(theta - w - w) * i_d * i_d
    y0 = amplitude * sin(theta - w ) * i_d

    while True:
        y2 = y0
        y0 = a1 * y0 - a2 * y1
        yield y0
        y1 = y0
        y0 = a1 * y0 - a2 * y2
        yield y0


def sinepings_gen(amplitudes, frequencies, decays, thetas=None, srate=None):
    if thetas is None:
        thetas = repeat(0)
    sps = [sineping_gen(*params) for params in zip(amplitudes, frequencies, decays, thetas, repeat(srate))]
    return mix_gen(sps)



def bl_sinepings_gen(amplitudes, frequencies, decays, thetas=None, srate=None):
    if srate is None:
        srate = get_srate()
    nyquist = 0.5 * srate

    if thetas is None:
        thetas = repeat(0)

    new_params = []
    for a, f, d, t in zip(amplitudes, frequencies, decays, thetas):
        if f < nyquist:
            new_params.append((a, f, d, t, srate))
    sps = [sineping_gen(*params) for params in new_params]
    return mix_gen(sps)


def bl_gen(coef_fun, freq_gen, srate=None, fade_bandwith=2000, max_partials=4000):
    if srate is None:
        srate = get_srate()
    nyquist = 0.5 * srate
    fade_start = nyquist - fade_bandwith
    i_fade_bandwith = 1.0 / fade_bandwith
    dt = 1.0 / srate
    t = 0.0
    phis = [0.0] * max_partials
    dphi = two_pi * dt
    for f in freq_gen:
        s = 0.0
        for k in range(1, max_partials + 1):
            amplitude, multiplier = coef_fun(k, f, t)
            partial_freq = f * multiplier
            if partial_freq > nyquist:
                break
            elif partial_freq > fade_start:
                amplitude *= 1.0 - (partial_freq - fade_start) * i_fade_bandwith
            s += sin(phis[k - 1]) * amplitude
            phis[k - 1] += dphi * partial_freq
        yield s
        t += dt


def saw_coefs(k, f, t):
    return (-0.4 / k, k)


def square_coefs(k, f, t):
    k = k + k - 1
    return (-0.6 / k, k)


def log_drum_coefs(k, f, t):
    return (0.2 * exp(-t * k) / k ** 1.5, log(k) + 1)
