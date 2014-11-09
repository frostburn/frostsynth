from math import *
from base import *
from filters.base import *


def decay(source, factor=0.01, duration=1.0, srate=None):
    """Exponential decay by 'factor' in time 'duration' when fed with a simple impulse."""
    if srate is None:
        srate = get_srate()
    return onepole(source, 1.0, -factor ** (srate / duration), 1.0)


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


#Filters from "Cookbook formulae for audio EQ biquad filter coefficients" by Robert Bristow-Johnson
#http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt

i_sqrt_two = 1.0 / sqrt(2.0)


def _lpf_coefs(frequency, Q, srate=None):
    if srate is None:
        srate = get_srate()
    w0 = 2.0 * pi * frequency / srate
    cosw0 = cos(w0)
    alpha = sin(w0) / (2.0 * Q)

    return (1.0 + alpha, -2.0 * cosw0, 1.0 - alpha, 0.5 * (1.0 - cosw0), 1.0 - cosw0, 0.5 * (1.0 - cosw0))


def lpf(source, frequency, Q=i_sqrt_two, srate=None):
    return biquad(source, *_lpf_coefs(frequency, Q, srate))


def dynamic_lpf(source, frequency, Q, srate=None):
    return dynamic_biquad(source, map(_lpf_coefs, frequency, Q, repeat(srate)))


def _hpf_coefs(frequency, Q, srate=None):
    if srate is None:
        srate = get_srate()
    w0 = 2.0 * pi * frequency / srate
    cosw0 = cos(w0)
    alpha = sin(w0) / (2.0 * Q)
    
    return (1.0 + alpha, -2.0 * cosw0, 1.0 - alpha, 0.5 * (1.0 + cosw0), -1.0 - cosw0, 0.5 * (1.0 + cosw0))


def hpf(source, frequency, Q=i_sqrt_two, srate=None):
    return biquad(source, *_hpf_coefs(frequency, Q, srate))


def dynamic_hpf(source, frequency, Q, srate=None):
    return dynamic_biquad(source, map(_hpf_coefs, frequency, Q, repeat(srate)))


if False:
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
        exec("""def _"""+name+"""_coefs(frequency, Q, srate=None):
        if srate is None:
            srate = get_srate()
        w0 = 2.0*pi*frequency/srate
        cosw0 = cos(w0)
        alpha = sin(w0)/(2.0*Q)"""+formula+"""  
        return (a0, a1, a2, b0, b1, b2)

    def """+name+"""(source, frequency, Q, srate=None):
        return biquad(source,*_"""+name+"""_coefs(frequency, Q, srate))

    def dynamic_"""+name+"""(source, frequency, Q, srate=None):
        return _dynamic_biquad(source, imap(_"""+name+"""_coefs, frequency, Q, repeat(srate)))""")

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
        w0 = 2.0*pi*frequency/srate
        cosw0 = cos(w0)
        alpha = sin(w0)/(2.0*Q)"""+formula+"""  
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