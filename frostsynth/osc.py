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
        phases.append((lambda s: integrate_gen(f * itofm(s + n * noise_spread) for f, n in zip(freq, noise)))(s))
    return [(lambda s: (p + s for p in phase))(shift) for phase, shift in zip(phases, shifts)]


def noisy_phases(frequency, spread=0.25, noise_spread=0.5, noise_speed=0.5, count=6):
    frequency = to_sequence(frequency)
    phases = []
    for s, shift in zip(linspace(-spread, spread, count), uniform(count, 0, 1)):
        noise = linear_noise(f * noise_speed for f in frequency)
        phases.append(integrate((f * itofm(s + n * noise_spread) for f, n in zip(frequency, noise)), shift))
    return phases


def noisy_wf(wf, frequency, spread=0.25, noise_spread=0.5, noise_speed=0.5, count=6):
    return gain(mix(map(wf, phase) for phase in noisy_phases(frequency, spread, noise_spread, noise_speed, count)), 0.4 / sqrt(count))


def noisy_saw(frequency, spread=0.25, noise_spread=0.5, noise_speed=0.5, count=6):
    return gain(mix(map(saw, phase) for phase in noisy_phases(frequency, spread, noise_spread, noise_speed, count)), 0.4 / sqrt(count))


def formant_gen(frequency, formant_frequency, width):
    f, temp = tee(to_iterable(frequency))
    i_f0, i_f1 = tee(1 / f for f in temp)
    r = (ff * i_f for ff, i_f in zip(to_iterable(formant_frequency), i_f0))
    w = (2 * w * i_f for w, i_f in zip(to_iterable(width), i_f1))
    return (theta_formant(p, r, w) for p, r, w in zip(integrate_gen(f), r, w))
