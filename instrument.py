from math import *
from cmath import exp as cexp

from base import *
from waveform import *
from filters import *
from envelope import *
from noise import *
from series import *
from additive import *

# TODO: Pass srate around correctly


def sine_beep(note):
    phase = integrate_gen(note.get_frequency_gen(), srate=note.srate)
    return [note.note_on_velocity * sine(p) for p in timeslice(phase, note.duration, srate=note.srate)]


def softsaw_bass(note):
    phase = integrate_gen(note.get_frequency_gen(), srate=note.srate)
    time_ = time(note.duration + 1, srate=note.srate)
    sharpness = decay_envelope_gen(0.75 + 0.25 * note.note_on_velocity, 1, srate=note.srate)
    return [
        (softsaw(p + 0.2 * t, s) + softsaw(p - 0.2 * t, s)) *
        note.note_on_velocity * 0.25 * exp(-t) * (tanh((note.duration - t) * (6 + note.note_off_velocity)) + 1.0)
        for t, p, s in zip(time_, phase, sharpness)
    ]


def simple_electric_piano(note):
    time_ = time(note.duration + 1)
    zs = [cexp(2j * pi * f * t) for t, f in zip(time_, note.get_frequency_gen())]
    zs = [(0.1 * z * cexp(0.9 * exp(-t * 2) * z) + 0.025 * z ** 5 * constant_series(0.8 * exp(-t * 10) * z ** 2)) * (1 + tanh((note.duration - t) * 20)) * tanh(t * 200) for t, z in zip(time_, zs)]
    return [z.real for z in zs]


def kick(percussion):
    return list(hpf([0.5 * cub((180 + percussion.velocity * 40) * exp(-t * 20.0) / 20.0) for t in time(0.25, srate=percussion.srate)], 20.0, srate=percussion.srate))


def snare(percussion):
    freqs = [200, 220, 300, 325, 335, 400, 450, 500, 550, 630]
    noise = list(lpf(uniform(1), 10000))
    hp_noise = decay_env_gen(hpf(noise, 2000), 0.05 + 0.07 * percussion.velocity, 25)
    noise = decay_env_gen(noise, 0.3, 15)

    drum_part = sinepings_gen([0.4 / k ** (1.2 - 0.4 * percussion.velocity) for k in range(1, 10)], freqs, [10 + f * 0.015 for f in freqs])

    return gain(mix([drum_part, noise, hp_noise]), 0.9 * percussion.velocity)


def hihat(percussion):
    noise = list(lpf(uniform(0.5), 15000))
    n400 = decay_env_gen(bpfQ(noise, 400, 3.0), 1.0, 15)
    n3000 = decay_env_gen(bpfQ(noise, 3000, 2.5), 0.5, 17)
    n6000 = decay_env_gen(bpfQ(noise, 6000, 2.5), 0.1 + percussion.velocity * 0.1, 16)
    n12000 = decay_env_gen(bpfQ(noise, 12000, 2.5), 0.1 + percussion.velocity * 0.1, 14)
    noise = decay_env_gen(noise, 1.0, 30)
    return gain(mix([noise, n400, n6000, n12000]), 0.3 * percussion.velocity)


percussion_bank = {
    36: kick,
    38: snare,
    42: hihat,
}
