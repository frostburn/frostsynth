from __future__ import division
from math import pi, sin, cos, sqrt
from sys import version_info


if version_info < (3,):
    from itertools import izip as zip


__author__ = "Lumi Pakkanen"
__copyright__ = "Copyright 2014, Lumi Pakkanen"
__credits__ = ["Lumi Pakkanen", "Robert Bristow-Johnson"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Lumi Pakkanen"
__email__ = "frostburn@suomi24.fi"
__status__ = "Initial release"

# All filters adapted from: http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt
# and factored into one-pole form.

__all__ = [
    'set_srate', 'get_srate',
    'dynamic_lowpass', 'dynamic_highpass',
    'dynamic_bandpass', 'dynamic_bandreject',
    'dynamic_allpass',
]

two_pi = 2 * pi

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


def _nyquist_twozero(source):
    source = iter(source)
    x2 = next(source)
    yield x2
    x1 = next(source)
    yield x1 + x2 + x2
    while True:
        x0 = next(source)
        yield x0 + x1 + x1 + x2
        x2 = next(source)
        yield x2 + x0 + x0 + x1
        x1 = next(source)
        yield x1 + x2 + x2 + x0


def dynamic_lowpass(source, frequency, Q, srate=None):
    """
    Dynamic low pass filter that doesn't suffer from transients.
    Normalized at DC.
    """
    srate = get_srate(srate)
    dw = two_pi / srate
    y0 = 0j
    for sample, f, q in zip(_nyquist_twozero(source), frequency, Q):
        w0 = dw * f
        cosw0 = cos(w0)
        alpha = sin(w0) / (2 * q)
        sqrt_discriminant = sqrt(1 - alpha * alpha - cosw0 * cosw0)
        a1 = (cosw0 + 1j * sqrt_discriminant) / (1 + alpha)
        b1 = 0.5 * (1.0 - cosw0) / sqrt_discriminant
        y0 = 1j * b1 * sample + a1 * y0
        yield y0.real


def _dc_twozero(source):
    source = iter(source)
    x2 = next(source)
    yield x2
    x1 = next(source)
    yield x1 - x2 - x2
    while True:
        x0 = next(source)
        yield x0 - x1 - x1 + x2
        x2 = next(source)
        yield x2 - x0 - x0 + x1
        x1 = next(source)
        yield x1 - x2 - x2 + x0


def dynamic_highpass(source, frequency, Q, srate=None):
    """
    Dynamic high pass filter that doesn't suffer from transients.
    Normalized at nyquist.
    """
    srate = get_srate(srate)
    dw = two_pi / srate
    y0 = 0j
    for sample, f, q in zip(_dc_twozero(source), frequency, Q):
        w0 = dw * f
        cosw0 = cos(w0)
        alpha = sin(w0) / (2 * q)
        sqrt_discriminant = sqrt(1 - alpha * alpha - cosw0 * cosw0)
        a1 = (cosw0 + 1j * sqrt_discriminant) / (1 + alpha)
        b1 = 0.5 * (1.0 + cosw0) / sqrt_discriminant
        y0 = 1j * b1 * sample + a1 * y0
        yield y0.real


def _dc_nyquist_twozero(source):
    source = iter(source)
    x2 = next(source)
    yield x2
    x1 = next(source)
    yield x1
    while True:
        x0 = next(source)
        yield x0 - x2
        x2 = next(source)
        yield x2 - x1
        x1 = next(source)
        yield x1 - x0


def dynamic_bandpass(source, frequency, Q, srate=None):
    """
    Dynamic band pass filter that doesn't suffer from transients.
    Peak amplitude normalized.
    """
    srate = get_srate(srate)
    dw = two_pi / srate
    y0 = 0j
    for sample, f, q in zip(_dc_nyquist_twozero(source), frequency, Q):
        w0 = dw * f
        cosw0 = cos(w0)
        alpha = sin(w0) / (2 * q)
        sqrt_discriminant = sqrt(1 - alpha * alpha - cosw0 * cosw0)
        a1 = (cosw0 + 1j * sqrt_discriminant) / (1 + alpha)
        b1 = alpha / sqrt_discriminant
        y0 = 1j * b1 * sample + a1 * y0
        yield y0.real


def dynamic_bandreject(source, frequency, Q, srate=None):
    """
    Dynamic band reject filter that doesn't suffer from transients.
    Normalized at DC and nyquist.
    """
    srate = get_srate(srate)
    dw = two_pi / srate
    y0 = 0j
    x1 = 0.0
    x2 = 0.0
    for sample, f, q in zip(source, frequency, Q):
        w0 = dw * f
        cosw0 = cos(w0)
        alpha = sin(w0) / (2 * q)
        sqrt_discriminant = sqrt(1 - alpha * alpha - cosw0 * cosw0)
        a1 = (cosw0 + 1j * sqrt_discriminant) / (1 + alpha)
        i_norm_j = 1j / sqrt_discriminant
        b2 = -2 * cosw0
        y0 = i_norm_j * (sample + b2 * x1 + x2) + a1 * y0
        yield y0.real
        x2 = x1
        x1 = sample


def dynamic_allpass(source, frequency, Q, srate=None):
    """
    Dynamic all pass filter that doesn't suffer from transients.
    """
    srate = get_srate(srate)
    dw = two_pi / srate
    y0 = 0j
    x1 = 0.0
    x2 = 0.0
    for sample, f, q in zip(source, frequency, Q):
        w0 = dw * f
        cosw0 = cos(w0)
        alpha = sin(w0) / (2 * q)
        sqrt_discriminant = sqrt(1 - alpha * alpha - cosw0 * cosw0)
        a1 = (cosw0 + 1j * sqrt_discriminant) / (1 + alpha)
        i_norm_j = 1j / sqrt_discriminant
        b1 = 1 - alpha
        b2 = -2 * cosw0
        b3 = 1 + alpha
        y0 = i_norm_j * (b1 * sample + b2 * x1 + b3 * x2) + a1 * y0
        yield y0.real
        x2 = x1
        x1 = sample
