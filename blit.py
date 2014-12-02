from math import *
from cmath import exp as cexp

from base import *


half_pi = 0.5 * pi


def sine_series(x, n):
    """
    Sum of n harmonics sin(2pi k x) with linear fading of the last harmonic for fractional values.
    For integer values use n + 1 to get full n harmonics.
    """
    floor_n = floor(n)
    mu = n - floor_n
    x *= pi
    floor_n_x = floor_n * x
    s = sin(floor_n_x)
    return -tan(x + half_pi) * s * s + sin(floor_n_x + floor_n_x) * (mu - 0.5)


def sineblit_gen(frequency, srate=None):
    nyquist = 0.5 * get_srate(srate)
    frequency, f = tee(to_iterable(frequency))
    phase = integrate_gen(f, srate=srate)
    for p, f in zip(phase, frequency):
        yield sine_series(p, nyquist / f)


def sineblit(frequency, srate=None):
    nyquist = 0.5 * get_srate(srate)
    phase = integrate(frequency, srate=srate)
    return [sine_series(p, nyquist / f) for p, f in zip(phase, frequency)]


def sine_series_odd(x, n):
    x *= two_pi
    s = sin(x)
    if abs(s) < epsilon:
        return s * n * n
    floor_n = floor(n)
    mu = n - floor_n
    floor_n *= 2.0 * x
    return (0.5 - 0.5 * cos(floor_n)) / s + sin(floor_n + x) * mu


def sineblit_odd_gen(frequency, srate=None):
    half_nyquist = 0.25 * get_srate(srate)
    frequency, f = tee(to_iterable(frequency))
    phase = integrate_gen(f, srate=srate)
    for p, f in zip(phase, frequency):
        yield sine_series_odd(p, half_nyquist / f - 0.5)


def sineblit_odd(frequency, srate=None):
    half_nyquist = 0.25 * get_srate(srate)
    phase = integrate(frequency, srate=srate)
    return [sine_series_odd(p, half_nyquist / f - 0.5) for p, f in zip(phase, frequency)]


def constant_series_n_mu(z, n):
    z1 = 1 - z
    if abs(z1) < epsilon:
        return n
    floor_n = floor(n)
    mu = n - floor_n
    z_floor_n = z ** floor_n
    return (1 - z_floor_n) / z1 + mu * z_floor_n


def blit_gen(frequency, sharpness=1.0, shift=0.0, phase=0.0, srate=None, leak_constant=0.95):
    srate = get_srate(srate)
    nyquist = 0.5 * srate
    frequency, f, f1 = tee(to_iterable(frequency), 3)
    sharpness, s = tee(to_iterable(sharpness))
    frequency_shift, fs = tee(to_iterable(shift))
    fs = (s * f for s, f in zip(fs, f1))
    phase_shift = to_iterable(phase)
    phase = integrate_gen(f, srate=srate)
    frequency_shift_phase = integrate_gen(fs, srate=srate)
    zs = (s * cexp(two_pi_j * p) for p, s in zip(phase, s))
    ms = (cexp(two_pi_j * (p + theta)) for p, theta in zip(frequency_shift_phase, phase_shift))
    return ((m * z * constant_series_n_mu(z, nyquist / f - 1 - fs)).real / s for z, m, f, s, fs in zip(zs, ms, frequency, sharpness, frequency_shift))


def blit(frequency, sharpness=1.0, shift=0.0, phase=0.0, srate=None):
    srate = get_srate(srate)
    nyquist = 0.5 * srate
    l = len(frequency)
    sharpness = to_sequence(sharpness, l)
    frequency_shift = to_sequence(shift, l)
    fs = (s * f for s, f in zip(frequency_shift, frequency))
    phase_shift = to_iterable(phase)
    phase = integrate_gen(frequency, srate=srate)
    frequency_shift_phase = integrate_gen(fs, srate=srate)
    zs = (s * cexp(two_pi_j * p) for p, s in zip(phase, sharpness))
    ms = (cexp(two_pi_j * (p + theta)) for p, theta in zip(frequency_shift_phase, phase_shift))
    return [(m * z * constant_series_n_mu(z, nyquist / f - 1 - fs)).real / s for z, m, f, s, fs in zip(zs, ms, frequency, sharpness, frequency_shift)]


def sawblit_gen(frequency, sharpness=1.0, shift=0.0, phase=0.0, srate=None, leak_constant=0.95):
    srate = get_srate(srate)
    gain = pi / srate
    frequency, f = tee(frequency)
    y = 0.5
    for x, f in zip(blit_gen(frequency, sharpness, shift, phase, srate), f):
        yield y
        y = leak_constant * y - gain * f * x


def sawblit(frequency, sharpness=1.0, shift=0.0, phase=0.0, srate=None, leak_constant=0.95):
    return list(sawblit_gen(frequency, sharpness, shift, phase, srate, leak_constant))
