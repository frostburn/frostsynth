from math import *
from cmath import rect as from_polar, exp as cexp

from base import *
from filters.base import *


def decay(source, factor=0.01, gain=1.0, duration=1.0, normalized=True, srate=None):
    """Exponential decay by 'factor' in time 'duration' when fed with a simple impulse."""
    srate = get_srate(srate)
    a1 = -factor ** (srate / duration)
    b0 = gain
    if normalized:
        b0 *= (1 + a1)
    return onepole(source, 1.0, a1, b0)


def attenuate(source, factor=0.01, duration=1.0, srate=None):
    """Exponential attenuation towards target value within 'factor' in time 'duration' for constant signals."""
    if srate is None:
        srate = get_srate()
    return onepole(source, 1.0, -factor ** (srate / duration), 1.0 - factor ** (srate / duration))


def dc_block(source, pole=0.995): #TODO: factor srate in
    """Removes the DC (zero frequency) component from the signal while trying to preserve other frequencies intact."""
    return polezero(source, 1.0, -pole, (1.0 + pole) * 0.5, -(1.0 + pole) * 0.5)


def allpass(source, g):
    """First order Shroeder all pass filter. y[n] + g y[n-1] = g.conjugate() x[n] + x[n-1]."""
    return polezero(source, 1.0, g.conjugate(), g, 1.0)


def ping_filter(source, frequency, decay, srate=None):
    """This filter responds to a unit impulse by producing a sinusoid "ping".

    The functional form of the response is: sin(2 * pi * frequency * t) * exp(-decay * t).
    """
    if srate is None:
        srate = get_srate()
    d = exp(-decay / srate)
    w = 2 * pi * frequency / srate
    return twopole(source, 1.0, -2.0 * d * cos(w), d * d, sin(w) * d)


def pong_filter(source, frequency, decay, srate=None):
    """This filter responds to a unit impulse by producing a hard sinusoid "ping".

    The functional form of the response is: cos(2*pi*frequency*t)*exp(-decay*t).
    """
    if srate is None:
        srate = get_srate()
    d = exp(-decay / srate)
    w = 2 * pi * frequency / srate
    return biquad(source, 1.0, -2.0 * d * cos(w), d * d, 1.0, -cos(w) * d, 0.0)


def onepole_lpf(source, d):
    return onepole(source, 1, -d, 1 - d)


#Filters from "Cookbook formulae for audio EQ biquad filter coefficients" by Robert Bristow-Johnson
#http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt

i_sqrt_two = 1.0 / sqrt(2.0)


def _lpf_coefs(frequency, Q, dw):
    w0 = dw * frequency
    cosw0 = cos(w0)
    alpha = sin(w0) / (2.0 * Q)
    cosw0_h = 0.5 * (1.0 - cosw0)

    return (1.0 + alpha, -2.0 * cosw0, 1.0 - alpha, cosw0_h, cosw0_h + cosw0_h, cosw0_h)


def lpf(source, frequency, Q=i_sqrt_two, srate=None):
    dw = two_pi / get_srate(srate)
    return biquad(source, *_lpf_coefs(frequency, Q, dw))


def dynamic_lpf(source, frequency, Q, srate=None):
    dw = two_pi / get_srate(srate)
    return dynamic_biquad(source, map(_lpf_coefs, frequency, Q, repeat(dw)))


def _hpf_coefs(frequency, Q, dw):
    w0 = dw * frequency
    cosw0 = cos(w0)
    alpha = sin(w0) / (2.0 * Q)
    cosw0_h = 0.5 * (1.0 + cosw0)

    return (1.0 + alpha, -2.0 * cosw0, 1.0 - alpha, cosw0_h, -cosw0_h - cosw0_h, cosw0_h)


def hpf(source, frequency, Q=i_sqrt_two, srate=None):
    dw = two_pi / get_srate(srate)
    return biquad(source, *_hpf_coefs(frequency, Q, dw))


def dynamic_hpf(source, frequency, Q, srate=None):
    dw = two_pi / get_srate(srate)
    return dynamic_biquad(source, map(_hpf_coefs, frequency, Q, repeat(dw)))


#Spam the rest using an exec macro:
_filter_names=["bpfQ", "bpf0", "notch", "apf"]

_filter_formulas=["""
    b0 =   Q*alpha
    b1 =   0
    b2 =  -Q*alpha
    a0 =   1 + alpha
    a1 =  -2*cosw0
    a2 =   1 - alpha""","""
    b0 =   alpha
    b1 =   0
    b2 =  -alpha
    a0 =   1 + alpha
    a1 =  -2*cosw0
    a2 =   1 - alpha""","""
    b0 =   1
    b1 =  -2*cosw0
    b2 =   1
    a0 =   1 + alpha
    a1 =  -2*cosw0
    a2 =   1 - alpha""","""
    b0 =   1 - alpha
    b1 =  -2*cosw0
    b2 =   1 + alpha
    a0 =   1 + alpha
    a1 =  -2*cosw0
    a2 =   1 - alpha"""]

for name, formula in zip(_filter_names, _filter_formulas):
    exec("def _" + name + """_coefs(frequency, Q, srate=None):
    if srate is None:
        srate = get_srate()
    w0 = two_pi * frequency / srate
    cosw0 = cos(w0)
    alpha = sin(w0) / (2.0 * Q)""" + formula + """
    return (a0, a1, a2, b0, b1, b2)


def """ + name + """(source, frequency, Q=i_sqrt_two, srate=None):
    return biquad(source, *_""" + name + """_coefs(frequency, Q, srate))


def dynamic_""" + name + """(source, frequency, Q, srate=None):
    return dynamic_biquad(source, map(_""" + name + """_coefs, frequency, Q, repeat(srate)))""")


if False:
    _filter_names=["peakingEQ", "lowshelf", "highshelf"]

    _filter_formulas=["""
        b0 =   1 + alpha*A
        b1 =  -2*cosw0
        b2 =   1 - alpha*A
        a0 =   1 + alpha/A
        a1 =  -2*cosw0
        a2 =   1 - alpha/A""","""
        b0 =    A*( (A+1) - (A-1)*cosw0 + 2*sqrtA*alpha )
        b1 =  2*A*( (A-1) - (A+1)*cosw0                   )
        b2 =    A*( (A+1) - (A-1)*cosw0 - 2*sqrtA*alpha )
        a0 =        (A+1) + (A-1)*cosw0 + 2*sqrtA*alpha
        a1 =   -2*( (A-1) + (A+1)*cosw0                   )
        a2 =        (A+1) + (A-1)*cosw0 - 2*sqrtA*alpha""","""
        b0 =    A*( (A+1) + (A-1)*cosw0 + 2*sqrtA*alpha )
        b1 = -2*A*( (A-1) + (A+1)*cosw0                   )
        b2 =    A*( (A+1) + (A-1)*cosw0 - 2*sqrtA*alpha )
        a0 =        (A+1) - (A-1)*cosw0 + 2*sqrtA*alpha
        a1 =    2*( (A-1) - (A+1)*cosw0                   )
        a2 =        (A+1) - (A-1)*cosw0 - 2*sqrtA*alpha"""]   

    for name, formula in zip(_filter_names, _filter_formulas):
        exec("""def _"""+name+"""_coefs(frequency, Q, A, srate=None):
        if srate is None:
            srate = get_srate()
        sqrtA = sqrt(A)
        w0 = two_pi * frequency / srate
        cosw0 = cos(w0)
        alpha = sin(w0) / (2.0 * Q)"""+formula+"""  
        return (a0, a1, a2, b0, b1, b2)

    def """+name+"""(source, frequency, Q, A, srate=None):
        return biquad(source,*_"""+name+"""_coefs(frequency, Q, A, srate))

    def dynamic_"""+name+"""(source, frequency, Q, A, srate=None):
        return _dynamic_biquad(source, imap(_"""+name+"""_coefs, frequency, Q, A, repeat(srate)))""")

    def dynamic_critical_lpf(source, time_constant, srate=None):
        """Low pass filter with impulse response proportional to t*exp(-t*time_constant).

        Normalized so that dynamic_critical_lpf(repeat(1), repeat(T)) approaches 1 for all values of T.
        """
        if srate is None:
            srate = get_srate()
        dt = 1.0/srate
        
        #Actually this is a dynamic TwoPole with a double pole at exp(-dt*T).
        source = iter(source) 
        c = (exp(-dt*T) for T in time_constant)

        d = next(c)
        x0 = next(source)
        y1 = x0 - (x0 + x0 - x0*d)*d
        yield y1
        d = next(c)
        x0 = next(source)
        y0 = x0 + (y1 + y1 - x0 - x0 + x0*d)*d
        yield y0
        
        while True:
            d = next(c)
            y2 = y0
            x0 = next(source)
            y0 = x0 + (y0 + y0 - x0 - x0 + (x0 - y1)*d)*d
            yield y0

            d = next(c)
            y1 = y0
            x0 = next(source)
            y0 = x0 + (y0 + y0 - x0 - x0 + (x0 - y2)*d)*d
            yield y0


def resonator(source, b1, frequency, decay, srate=None):
    """
    Delayed resonant filter.
    Peak amplitude_normalized.
    """
    srate = get_srate(srate)
    dt = 1 / srate
    z = from_polar(1, -two_pi * frequency * dt)
    a1 = exp(-decay * frequency * dt) * z
    b1 *= 2j / abs(1j / (1 - a1 * z) - 1j / (1 - a1.conjugate() * z))
    y0 = 0.0j
    for sample in source:
        y0 = b1 * sample + y0 * a1
        yield y0.real


def dynamic_resonator(source, b1, frequency, decay, srate=None):
    """
    Delayed dynamic resonant filter that doesn't suffer from transients.
    Peak amplitude normalized.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
    srate = get_srate(srate)
    dt = 1 / srate
    y0 = 0.0j
    for sample, b, f, d in zip(source, b1, frequency, decay):
        z = from_polar(1, -two_pi * f * dt)
        a1 = exp(-d * f * dt) * z
        i_norm_j = 2j / abs(1j / (1 - a1 * z) - 1j / (1 - a1.conjugate() * z))
        y0 = i_norm_j * b * sample + y0 * a1
        yield y0.real


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


def dynamic_lowpass(source, frequency, Q=i_sqrt_two, srate=None):
    """
    Dynamic low pass filter that doesn't suffer from transients.
    Normalized at DC.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
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


def dynamic_highpass(source, frequency, Q=i_sqrt_two, srate=None):
    """
    Dynamic high pass filter that doesn't suffer from transients.
    Normalized at nyquist.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
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


def dynamic_bandpass(source, frequency, Q=i_sqrt_two, srate=None):
    """
    Dynamic band pass filter that doesn't suffer from transients.
    Peak amplitude normalized.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
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


def dynamic_allpass(source, frequency, Q=i_sqrt_two, srate=None):
    """
    Dynamic all pass filter that doesn't suffer from transients.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
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


def dynamic_bandreject(source, frequency, Q=i_sqrt_two, srate=None):
    """
    Dynamic band reject filter that doesn't suffer from transients.
    Normalized at DC and nyquist.
    """
    frequency = to_iterable(frequency)
    Q = to_iterable(Q)
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
