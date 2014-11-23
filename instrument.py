from math import *
from cmath import exp as cexp

from base import *
from waveform import *
from filters import *
from envelope import *
from noise import *
from series import *
from additive import *
from analysis import *
from resample import *

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


def bass(note):
    phase = integrate_gen(note.get_frequency_gen(), srate=note.srate)
    m = 4.0 + exp(-note.frequency)
    return [note.note_on_velocity * 0.3 * pen(p * m + pen(p) * exp(-5 * t) * (0.5 + note.note_on_velocity)) * exp(-6 * t) * (tanh((note.duration - t) * (6 + note.note_off_velocity)) + 1.0) for t, p in zip(time(2), phase)]


def simple_electric_piano(note):
    time_ = time(note.duration + 1)
    zs = [cexp(2j * pi * f * t) for t, f in zip(time_, note.get_frequency_gen())]
    zs = [(0.1 * z * cexp(0.9 * exp(-t * 2) * z) + 0.025 * z ** 5 * constant_series(0.8 * exp(-t * 10) * z ** 2)) * (1 + tanh((note.duration - t) * 20)) * tanh(t * 200) for t, z in zip(time_, zs)]
    return [z.real for z in zs]


def organ(note):
    # TODO: note.srate
    freq = note.frequency

    w = []
    for f in freq_window(1 << 16):
        s = 0.0
        for e in range(16):
            p = exp(-0.02 * (f - freq * 2 ** e) ** 2)
            p += exp(-0.02 * (f - freq * 3 ** e) ** 2) * 0.8 / (e + 1)
            p += exp(-0.02 * (f - freq * 5 ** e) ** 2) * 0.4 / (e + 1)
            if e > 3:
                p /= (e - 3) ** 2
            s += p
        s += exp(-0.02 * (f - 6 * freq) ** 2) * 0.5
        s += exp(-0.02 * (f - 10 * freq) ** 2) * 0.2
        w.append(cunit() * s * 5)


    s = pseudo_norm_irfft(w)

    s = cycle(s)

    ratio = (freq / f for f in note.get_frequency_gen())

    return hold_release_env(resampler1_gen(s, ratio), note.duration, 0.1 - 0.04 * note.note_off_velocity)


def dirty_steel_drum(note):
    t = note.duration + 1
    s = zero_t(t)
    time_ = time(t)
    velocity = note.note_on_velocity

    for i, p in zip(range(len(s)), integrate_gen(note.get_frequency_gen())):
        t = time_[i]
        s[i] = cub(p + 0.15 * velocity * exp(-t * 7) * s[i - 500] + 0.12 * s[int(i//1.99) - 199] + 0.1 * s[int(i//3.01) - 2000]) * (tanh(note.duration - t) + 1.0) * velocity

    return s


def log_drum(note):
    num_partials = 50
    r = list(range(1, num_partials + 1))
    return hold_release_env(
        bl_sinepings_gen(
            [note.note_on_velocity * 0.4 / k ** (2.0 - note.note_on_velocity * 0.8) for k in r],
            [note.frequency * (log(k) + 1) for k in r],
            [2 + k for k in r],
            [5 * (k - 1) ** 1.9 for k in r],
            srate=note.srate
        ),
        note.duration, 0.15 - 0.05 * note.note_off_velocity,
        srate=note.srate
    )


def kick(percussion):
    return list(hpf([0.5 * cub((180 + percussion.velocity * 40) * exp(-t * 20.0) / 20.0) for t in time(0.25, srate=percussion.srate)], 20.0, srate=percussion.srate))


def snare(percussion):
    freqs = [200, 220, 300, 325, 335, 400, 450, 500, 550, 630]
    noise = list(lpf(uniform_t(1), 10000))
    hp_noise = decay_env_gen(hpf(noise, 2000), 0.05 + 0.07 * percussion.velocity, 25)
    noise = decay_env_gen(noise, 0.3, 15)

    drum_part = sinepings_gen([0.4 / k ** (1.2 - 0.4 * percussion.velocity) for k in range(1, 10)], freqs, [10 + f * 0.015 for f in freqs])

    return gain(mix([drum_part, noise, hp_noise]), 0.9 * percussion.velocity)


def hihat(percussion):
    noise = list(lpf(uniform_t(0.5), 15000))
    n400 = decay_env_gen(bpfQ(noise, 400, 3.0), 1.0, 15)
    n3000 = decay_env_gen(bpfQ(noise, 3000, 2.5), 0.5, 17)
    n6000 = decay_env_gen(bpfQ(noise, 6000, 2.5), 0.1 + percussion.velocity * 0.1, 16)
    n12000 = decay_env_gen(bpfQ(noise, 12000, 2.5), 0.1 + percussion.velocity * 0.1, 14)
    noise = decay_env_gen(noise, 1.0, 30)
    return gain(mix([noise, n400, n6000, n12000]), 0.3 * percussion.velocity)


def hihat2(percussion):
    def train_g():
        noise = fast_uniform_t(0.4)
        train = fft_train(noise, include_time=True)
        for t, window in train:
            result = []
            for f, n in freq_enumerate(window):
                x = f / 20000.0
                result.append(percussion.velocity * 30 * n * (0.25 + sin(143 * x + 4 * cos(104 * x)) ** 4) * x * exp(-(8 - percussion.velocity) * x) * fast_uniform() ** 2 * exp(-15 * t * (0.5 * x + 1)))
            yield result

    return list(ifft_train(train_g()))


percussion_bank = {
    36: kick,
    38: snare,
    42: hihat2,
}
