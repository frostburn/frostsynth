from math import cos, pi
from cmath import polar
from fft import *

from base import get_srate


def delta_phi(phi1, phi2):
    delta = phi2 - phi1
    if delta < -pi:
        delta += 2 * pi
    elif delta > pi:
        delta -= 2 * pi
    return delta


def unwrap_phase(phis):
    result = [0.0] * len(phis)
    running_total = 0.0
    inverse_two_pi = 0.5 / pi
    for i in range(len(phis) - 1):
        running_total += delta_phi(phis[i + 1], phis[i]) * inverse_two_pi # Reversed and normalized to get a positive phase signal in the most common use case.
        result[i + 1] = running_total
    return result


def polar_decomposition(signal):
    """Returns the polar decomposition of a real-valued sinusoidal signal."""
    padded_signal = pad(signal)
    rdft = rfft(padded_signal)
    ps = [polar(z) for z in ifft(rdft + [0.0] * (len(rdft) - 2))[:len(signal)]]
    rs, phis = zip(*ps)
    return zip(rs, unwrap_phase(phis))


def fft_train(signal, window_size=4096, include_time=False):
    if window_size < 4:
        raise ValueError("Too small window_size.")
    if window_size & (window_size - 1) != 0:
        raise ValueError("Only power of two window_sizes supported.")
    pad_size = window_size // 4
    window_function = [0.0] * pad_size + [1.0 - cos(2 * pi * i / (2 * pad_size)) for i in range(pad_size * 2)] + [0.0] * pad_size
    assert(len(window_function) == window_size)
    signal = [0.0] * 2 * pad_size + signal + [0.0] * 2 * pad_size
    if (len(signal) % window_size != 0):
        signal += [0.0] * (window_size - len(signal) % window_size)
    assert(len(signal) % window_size == 0)
    dt = 1.0 / get_srate()
    for i in range(0, len(signal) - pad_size * 3, pad_size):
        window = [s * w for s, w in zip(signal[i: i + window_size], window_function)]
        rdft = rfft(window)
        if include_time:
            yield ((i - 2 * pad_size) * dt, rdft)
        else:
            yield rdft


def ifft_train(train):
    result = irfft(next(train))
    M = 3 * len(result) // 4
    for window in train:
        signal = irfft(window)
        result[-M:] = [r + s for r, s in zip(result[-M:], signal[:M])]
        result += signal[M:]
    return result


def freq_enumerate(window):
    srate = get_srate()
    df = srate / (len(window) * 2 - 1)
    return [(i * df, b) for i, b in enumerate(window)]
