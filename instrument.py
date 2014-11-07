from math import *

from base import *
from waveform import *

def softsaw_bass(time, freq, velocity=1.0, duration=1.0):
    phase = integrate(freq)
    sharpness = [exp(-t) * (0.75 + 0.25 * velocity) for t in time]
    return [(softsaw(p + 0.2 * t, s) + softsaw(p - 0.2 * t, s)) * velocity * 0.25 * exp(-t) * (tanh((duration - t) * 6) + 1.0) for (t, p, s) in zip(time, phase, sharpness)]
