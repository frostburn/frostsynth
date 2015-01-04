from math import *
from cmath import rect as from_polar
from itertools import *

from frostsynth import *
from frostsynth.fft import *
from frostsynth.polytable import *


four_pi = 4 * pi


def sineping_gen(amplitude, frequency, decay, phi=0, srate=None):
    """Generates amplitude * sin(2 * pi * t * frequency + phi) * exp(-t * decay)."""
    srate = get_srate(srate)

    dt = 1 / srate


    d = exp(-dt * decay)
    w = two_pi * dt * frequency

    a1 = 2 * d * cos(w)
    a2 = d * d

    y1 = amplitude * sin(phi)
    yield y1

    y0 = amplitude * sin(phi + w) * d
    yield y0

    while True:
        y2 = y0
        y0 = a1 * y0 - a2 * y1
        yield y0
        y1 = y0
        y0 = a1 * y0 - a2 * y2
        yield y0


def sinepings_gen(amplitudes, frequencies, decays, phis=None, srate=None):
    if phis is None:
        phis = repeat(0)
    sps = [sineping_gen(*params) for params in zip(amplitudes, frequencies, decays, phis, repeat(srate))]
    return mix_gen(sps)


def sinepings(amplitudes, frequencies, decays, phis=None, accuracy_goal=1e-4, srate=None):
    duration_constant = -log(accuracy_goal)
    if phis is None:
        phis = repeat(0)
    sps = [timeslice_gen(sineping_gen(*params), duration_constant / params[2], srate=srate) for params in zip(amplitudes, frequencies, decays, phis, repeat(srate))]
    return mix_longest(sps)


def bl_sinepings_gen(amplitudes, frequencies, decays, phis=None, srate=None):
    if srate is None:
        srate = get_srate()
    nyquist = 0.5 * srate

    if phis is None:
        phis = repeat(0)

    new_params = []
    for a, f, d, t in zip(amplitudes, frequencies, decays, phis):
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


def irfft_waveform(window):
    derivates_window = [two_pi_j * b * i for i, b in enumerate(window)]
    window = rpad(window + [0.0] * len(window))
    derivates_window = rpad(derivates_window + [0.0] * len(derivates_window))
    values = unnormalized_irfft(window)
    derivatives = irfft(derivates_window)
    ct = CubicTable(zip(values, derivatives), periodic=True)
    l = len(ct)
    return lambda p: ct(p * l)


def irfft_waveform2(windows, periodic_y=False):
    data = []
    for window in windows:
        derivates_window = [two_pi_j * b * i for i, b in enumerate(window)]
        window = rpad(window + [0.0] * len(window))
        derivates_window = rpad(derivates_window + [0.0] * len(derivates_window))
        values = unnormalized_irfft(window)
        derivatives = irfft(derivates_window)
        data.append(zip(values, derivatives))
    xct = XCubicTable2D(data, periodic_x=True, periodic_y=periodic_y)
    lx = xct.len_x
    ly = xct.len_y
    if periodic_y:
        return lambda p, s: xct(p * lx, s * ly)
    else:
        ly -= 2
        return lambda p, s: xct(p * lx, s * ly)


# TODO: Fade bandwidth.
def irfft_osc_gen(frequency, windows, dt=0.1, srate=None):
    srate = get_srate(srate)
    nyquist = 0.5 * srate
    dt_ = 1.0 / srate
    i_dt = 1.0 / dt
    frequency = iter(frequency)
    if isinstance(windows, Sequence):
        if not isinstance(windows[0], Sequence):
            windows = repeat(windows)
    windows = iter(windows)
    f = next(frequency)
    window1 = [b for i, b in enumerate(next(windows)) if i * f < nyquist]
    wf1 = irfft_waveform(window1)
    yield wf1(0)
    t = dt + dt_
    phase = dt_ * f
    for f in frequency:
        if t > dt:
            wf0 = wf1
            window1 = [b for i, b in enumerate(next(windows)) if i * f < nyquist]
            wf1 = irfft_waveform(window1)
            t -= dt
        w0 = wf0(phase)
        yield w0 + t * i_dt * (wf1(phase) - w0)
        phase += dt_ * f
        t += dt_


def cos_sum(phase, coefs):
    """Evaluates sum(coef * cos(2 * pi * k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0]
    elif len(coefs) == 2:
        return coefs[0] + coefs[1] * cos(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        c2 = c + c
        bk = coefs[-1]
        bk1 = coefs[-2] + c2 * bk
        for coef in coefs[-3:0:-1]:
            bk1, bk = coef + c2 * bk1 - bk, bk1
        return coefs[0] + c * bk1 - bk


def cos_octave_sum(phase, coefs):
    """Evaluates sum(coef * cos(2 * pi * 2 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * cos(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        result = coefs[0] * c
        for coef in coefs[1:]:
            c = 2 * c * c - 1
            result += coef * c
        return result


def sin_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * k * phase) for k, coef in enumerate(coefs, 1))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    elif len(coefs) == 2:
        return coefs[0] * sin(two_pi * phase) + coefs[1] * sin(four_pi * phase)
    else:
        c2 = 2 * cos(two_pi * phase)
        bk = coefs[-1]
        bk1 = coefs[-2] + c2 * bk
        for coef in coefs[-3:0:-1]:
            bk1, bk = coef + c2 * bk1 - bk, bk1
        return sin(two_pi * phase) * (coefs[0] + c2 * bk1 - bk)


def sin_odd_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * (2 * k - 1) * phase) for k, coef in enumerate(coefs, 1))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        s = sin(two_pi * phase)
        s2 = 2 - 4 * s * s
        bk = coefs[-1]
        bk1 = coefs[-2] + s2 * bk
        for coef in coefs[-3::-1]:
            bk1, bk = coef + s2 * bk1 - bk, bk1
        return s * (bk1 + bk)


def sin_octave_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * 2 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        c = cos(two_pi * phase)
        s = sin(two_pi * phase)
        result = coefs[0] * s
        s *= c + c
        result += coefs[1] * s
        for coef in coefs[2:]:
            c = 2 * c * c - 1
            s *= c + c
            result += coef * s
        return result


def sin_tritave_sum(phase, coefs):
    """Evaluates sum(coef * sin(2 * pi * 3 ** k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0
    elif len(coefs) == 1:
        return coefs[0] * sin(two_pi * phase)
    else:
        s = sin(two_pi * phase)
        result = coefs[0] * s
        for coef in coefs[1:]:
            s = s * (3 - 4 * s * s)
            result += coef * s
        return result


def cis_sum(phase, coefs, sharpness=1):
    """Evaluates sum(coef * exp(2j * pi * k * phase) for k, coef in enumerate(coefs, 0))."""
    if not coefs:
        return 0j
    else:
        z = from_polar(sharpness, two_pi * phase)
        result = coefs[-1]
        for coef in coefs[-2::-1]:
            result = coef + z * result
        return result
