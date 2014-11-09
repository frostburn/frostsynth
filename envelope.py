from math import *

from base import *

def decay_envelope_gen(amplitude, decay, srate=None):
    """
    Generates amplitude * exp(-t * decay)
    """
    if srate is None:
        srate = get_srate()
    d = exp(-decay / srate)
    y0 = amplitude
    while True:
        yield y0
        y0 *= d

def decay_env_gen(source, amplitude, decay, srate=None):
    envelope = decay_envelope_gen(amplitude, decay, srate)
    return (s * e for s, e in zip(source, envelope))
