from math import *

from frostsynth import *
from frostsynth.noise import *
from frostsynth.waveform import *
from frostsynth.track import *

def sinehorn_gen(freq, sharpness):
    dt = 2 * pi / get_srate()
    phase = 0.0
    value = 0.0
    for f, s in zip(freq, sharpness):
        s = clip(s, -0.99, 0.99)
        phase += dt * f * (1 + s * value) * (1.0 - s * s) ** -0.5
        value = sin(phase)
        yield value


def noisy_saw_gen(frequency, spread=0.25, noise_spread=0.25, noise_speed=0.5, order=6):
    frequency = to_iterable(frequency)
    scale = 0.4 * sqrt(1.0 / order)
    shifts = uniform(order)
    phases = []
    for s, freq in zip(linspace(-spread, spread, order), tee(frequency, order)):
        f, freq = tee(freq)
        noise = snow3_gen((f * noise_speed for f in f), variability=0.5)
        phases.append((lambda s: integrate_gen(f * itom(s + n * noise_spread) for f, n in zip(freq, noise)))(s))
    return mix_gen((lambda s: (saw(p + s) * scale for p in phase))(shift) for phase, shift in zip(phases, shifts))


def noisy_saw(frequency, spread=0.25, noise_spread=0.25, noise_speed=0.5, order=6):
    scale = 0.4 * sqrt(1.0 / order)
    shifts = uniform(order)
    phases = []
    for s in linspace(-spread, spread, order):
        noise = snow3([f * noise_speed for f in frequency], variability=0.5)
        phases.append(integrate(f * itom(s + n * noise_spread) for f, n in zip(frequency, noise)))
    return mix([saw(p + s) * scale for p in phase] for phase, s in zip(phases, shifts))
