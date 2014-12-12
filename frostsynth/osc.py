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


def noisy_phases_gen(frequency, spread=0.25, noise_spread=0.25, noise_speed=0.5, count=6):
    frequency = to_iterable(frequency)
    shifts = uniform(count, 0, 1)
    phases = []
    for s, freq in zip(linspace(-spread, spread, count), tee(frequency, count)):
        f, freq = tee(freq)
        noise = snow3_gen((f * noise_speed for f in f), variability=0.5)
        phases.append((lambda s: integrate_gen(f * itom(s + n * noise_spread) for f, n in zip(freq, noise)))(s))
    return [(lambda s: (p + s for p in phase))(shift) for phase, shift in zip(phases, shifts)]


def noisy_phases(frequency, spread=0.25, noise_spread=0.25, noise_speed=0.5, count=6):
    shifts = uniform(count, 0, 1)
    phases = []
    for s in linspace(-spread, spread, count):
        noise = snow3([f * noise_speed for f in frequency], variability=0.5)
        phases.append(integrate(f * itom(s + n * noise_spread) for f, n in zip(frequency, noise)))
    return [[p + s for p in phase] for phase, s in zip(phases, shifts)]


def noisy_saw(frequency, spread=0.25, noise_spread=0.25, noise_speed=0.5, count=6):
    return gain(mix(map(saw, phase) for phase in noisy_phases(frequency, spread, noise_spread, noise_speed, count)), 0.4 / sqrt(count))
