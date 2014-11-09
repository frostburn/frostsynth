from math import *

from base import *
from waveform import *
from filters import *
from envelope import *
from noise import *
from additive import *


def softsaw_bass(note):
    phase = integrate_gen(note.get_frequency_gen(), srate=note.srate)
    time_ = time(note.duration + 1, srate=note.srate)
    sharpness = decay_envelope_gen(0.75 + 0.25 * note.note_on_velocity, 1, srate=note.srate)
    return [
        (softsaw(p + 0.2 * t, s) + softsaw(p - 0.2 * t, s)) *
        note.note_on_velocity * 0.25 * exp(-t) * (tanh((note.duration - t) * (6 + note.note_off_velocity)) + 1.0)
        for t, p, s in zip(time_, phase, sharpness)
    ]

def sine_beep(note):
    phase = integrate_gen(note.get_frequency_gen(), srate=note.srate)
    return [note.note_on_velocity * sine(p) for p in timeslice(phase, note.duration, srate=note.srate)]

def snare():
    freqs = [200, 220, 300, 325, 335, 400, 450, 500, 550, 630]
    noise = list(lpf(uniform(1), 10000))
    hp_noise = decay_env_gen(hpf(noise, 2000), 0.1, 25)
    noise = decay_env_gen(noise, 0.3, 15)

    drum_part = sinepings_gen([0.3 / k for k in range(1, 10)], freqs, [10 + f * 0.015 for f in freqs])

    return mix([drum_part, noise, hp_noise])
