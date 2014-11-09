from math import *

from base import *
from waveform import *
from filters import *
from envelope import *
from noise import *
from additive import *


def softsaw_bass(time, freq, velocity=1.0, duration=1.0):
    phase = integrate(freq)
    sharpness = [exp(-t) * (0.75 + 0.25 * velocity) for t in time]
    return [(softsaw(p + 0.2 * t, s) + softsaw(p - 0.2 * t, s)) * velocity * 0.25 * exp(-t) * (tanh((duration - t) * 6) + 1.0) for (t, p, s) in zip(time, phase, sharpness)]


def snare():
    freqs = [200, 220, 300, 325, 335, 400, 450, 500, 550, 630]
    noise = list(lpf(uniform(1), 10000))
    hp_noise = decay_env_gen(hpf(noise, 2000), 0.1, 25)
    noise = decay_env_gen(noise, 0.3, 15)

    drum_part = sinepings_gen([0.3 / k for k in range(1, 10)], freqs, [10 + f * 0.015 for f in freqs])

    return mix([drum_part, noise, hp_noise])
