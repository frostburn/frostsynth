from itertools import *
from math import *
from random import *
from cmath import exp as cexp, log as clog

from base import *
from fft import *
from waveform import *
from instrument import *
from analysis import *
from series import *
from osc import *
from filters import *
from noise import *
from additive import *
from envelope import *
from track import *
from aplayout import play
import wavein
from waveout import save

srate = get_srate()

#s = [0.5 * tanh(tanh(sin(1300.0 * sqrt(t)) * 5) + tanh(sin(1300 * 1.5 * sqrt(t) + 3 * t) * 5) * 0.6 + tanh(sin(1300 * 2 * sqrt(t) + 1.776*t) * 5) * 0.3) for t in time(7)]

#play(s)

#fs = [exp(-0.0001*(b - 300)**2) * (0.5 + 0.5 * cos(b * 0.01))**3 * cexp(2 * pi * random()) for b in range(1 << 15)]

#fs += [0] * len(fs)

#play([z.real * 0.005 for z in fft(fs)])

#t = time(3)
#f = [55 for t in time(3)]

#track = Track([(A3, 1), C4, Ds5, D5])

#play(sequencer(softsaw_bass, track))

#loglist = [log(i + 1) for i in range(10000000)]
#print(sum(loglist))

#t = time(1)
#f = [440.0] * len(t)

#print(sum(softsaw_bass(t, f)))

#t = time_gen()
#f = repeat(440.0)


#def softsaw_bass_gen(time, freq, velocity=1.0, duration=1.0):
#    phase = integrate_gen(freq)
#    sharpness = (exp(-t) * (0.75 + 0.25 * velocity) for t in time)
#    return ((softsaw(p + 0.2 * t, s) + softsaw(p - 0.2 * t, s)) * velocity * 0.25 * exp(-t) * (tanh((duration - t) * 6) + 1.0) for (t, p, s) in zip(time, phase, sharpness))

#s = softsaw_bass_gen(t, f)

#print(sum(islice(s, 100)))

#print(sum(timeslice(s, 100)))

#f = wavein.open("zelda_whistle.wav")

#def sine5(p, r):
#    x = p * 2 * pi
#    return sin(x + sin(x * 5) * r * 0.5 + sin(x * 3) * r * 0.2)

#s = [r * sine5(p, r) for r, p in polar_decomposition(f)]

#s = [(220.0 * t - floor(220.0 * t)) - 0.5 for t in time(3)]

#train = fft_train(s)
#s = ifft_train([0.5 * b * exp(-((f - i * 30) * 0.001)**2) for f, b in freq_enumerate(window)] for i, window in enumerate(train))

#from experiments.hilbert import *

#"""
#def sine(x):
#    return sin(2 * pi * x)

#s = [0.4 * (
#    sine(t * 260 * (1 - t * 0.05) + 0.5 * sin(t * 117) * exp(-20 * t) + 0.6 * sin(t * 299) * exp(-8 * t) + sine(341 * t) * exp(-1 * t) * 0.01) * exp(-11 * t) + random() * exp(-10 * t)
#)for t in time(3)]

#s = [0.5 * (cub_complement(t * 220) * cos(500 * t * t) + cub(t * 220) * sin(500 * t * t)) for t in time(5)]

#print(linear_series(0.999999, 1.0, 1.0, 5))

#zs = [cexp(1j * t * 6.283 * 220) for t in time(5)]

#ss = [z * power_series(z*z, [1 * exp(-t * 2), 0.5 * exp(-t * 3), exp(-10 * t), 0.3 * exp(-3*t), 0.2 * exp(-5 * t), 0.1 * exp(-20 * t)]) + 0.1 * z**7 * constant_series(0.5 * z) * exp(-20 * t) for t, z in zip(time(5), zs)]

#ss = [demiharmonic_series(z) for z in zs]

#s = [0.5 * s.real for s in ss]

#s = [v for v in sinehorn_gen(repeat(1000), [0.3 + 6 * (t + 0.1) * exp(-5 * t) for t in time(3)])]
#s = [sine(1000 * t) for t in time(1)] + s



#s = mix([[0.1 * sine(f * t) * exp(-10 * t * f * 0.01) for t in time(2)] for f in freqs], [1 / k for k in range(1, 10)])

#for i in range(1000):
#    n = uniform(1)

note_list = [AbsoluteNote(pitch=D3, note_on_time=0.0, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Ab3, note_on_time=0.375, note_on_velocity=0.787401574803, duration=0.375, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=0.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=D3, note_on_time=1.25, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=B3, note_on_time=1.5, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=1.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Ab3, note_on_time=2.0, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=2.25, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Ab3, note_on_time=2.5, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=2.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Db3, note_on_time=3.75, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=D3, note_on_time=4.0, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Ab3, note_on_time=4.375, note_on_velocity=0.787401574803, duration=0.375, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=4.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=D3, note_on_time=5.25, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=B3, note_on_time=5.5, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=5.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Ab3, note_on_time=6.0, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=A3, note_on_time=6.25, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0),
 AbsoluteNote(pitch=Gb3, note_on_time=6.5, note_on_velocity=0.787401574803, duration=0.25, note_off_velocity=1.0),
 AbsoluteNote(pitch=D3, note_on_time=6.75, note_on_velocity=0.787401574803, duration=0.125, note_off_velocity=1.0)]

percussion_list = [AbsolutePercussion(index=42, note_on_time=0.0, velocity=0.787401574803),
 AbsolutePercussion(index=36, note_on_time=0.0, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=0.25, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=0.5, velocity=0.787401574803),
 AbsolutePercussion(index=38, note_on_time=0.5, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=0.75, velocity=0.787401574803),
 AbsolutePercussion(index=36, note_on_time=0.75, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=1.0, velocity=0.787401574803),
 AbsolutePercussion(index=36, note_on_time=1.0, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=1.25, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=1.5, velocity=0.787401574803),
 AbsolutePercussion(index=38, note_on_time=1.5, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=1.75, velocity=0.787401574803)]



#s = note_list_to_sound(note_list, dirty_steel_drum)

#s = gain(s, 0.3)

#p = percussion_list_to_sound(loop(percussion_list, 4, 2.0), percussion_bank)

#s = gain(merge(s, p, 0), 0.5)


#s = softsaw_bass(AbsoluteNote(pitch=E4, note_on_time=0.0, note_on_velocity=0.566929133858, duration=0.525, note_off_velocity=0.0))

#print(s)

#perc = Percussion(velocity=0.787401574803)

#s = gain(snare(perc) + zero(2), 0.7)

#s = schroeder_t(s, 0.01, 0.4)

#s = schroeder_t(s, 0.017, 0.3)


#s = list(reverb(s))

#s = timeslice(s, 2)

#l = [1] + [0] * 10

#cs = filtered_comb(l, 3, lambda s: onepole_lpf(s, 0.5))

#print(list(cs))
"""
dt = 1.0 / get_srate()

s = [exp(-2000000 * (t - 0.01) ** 2) for t in time(0.02)] + zero(3)

def signal():
    for i in range(len(s)):
        t = i * dt
        yield cub(t * 220 + 0.3 * s[i - 21]) * s[i - 102] * 1.6
d = lpf(dc_block(signal()), 1000)
#d = signal()

for i in range(len(s)):
    s[i] = s[i] + next(d)

s = gain(s, 0.5)
"""

"""
s = wavein.open("cymbal.wav")

s += zero((len(s) // 4096 + 1) * 4096 - len(s))

n = uniform(len(s))

train = [[abs(z) for z in w] for w in fft_train(s, window_size=1024, windowing=False)]
#n_train = fft_train(n, window_size=1024)
#s = ifft_train([0.05 * sz * nz for sz, nz in zip(sw, nw)] for sw, nw in zip(train, n_train))

#sw = [sum(t) for t in zip(*train[:5])]
print(len(train))
sw = train[3]
n_train = fft_train(n, window_size=1024, include_time=True)
s = ifft_train([random() * 0.1 * abs(sz) * nz * exp(-t * 5) for sz, nz in zip(sw, nw)] for t, nw in n_train)
"""


def train_g():
    noise = list(hpf(hpf(timeslice(wavein.open("heivaan.wav"), 0.5, 2.1), 500), 500))
    train = fft_train(noise, include_time=True)
    p = [par(220 * t + cos(3.5 * t) * 10) for t in time_k(len(noise))]
    p_train = fft_train(p)
    for (t, window), pwindow in zip(train, p_train):
        result = []
        for n, p in zip(window, pwindow):
            t0 = (t - 0.15) * 4
            t1 = (t - 0.95) * 6
            t2 = (t - 1.4) * 4
            mu = (exp(-t0**2) + exp(-t1**2) + exp(-t2 ** 2) ) * 0.7
            np = abs(n) * p
            result.append(np + mu * (n - np))
        yield result


#s = ifft_train(train_g())
#s = gain(s, 0.38)

#f = 220

#s = [4.5 * pen(f * t + 0.1 * cub(2 * f * t) * exp(-3 * t)) * exp(-4 * t)  for t in time(2)]

#s = onezero(s, 1.0, -1.0, 1.0)

#note = AbsoluteNote(pitch=D4, note_on_time=1.25, note_on_velocity=0.787401574803, duration=2.125, note_off_velocity=1.0)

#s = list(bl_gen(log_drum_coefs, [220.0 for t in time(4)], max_partials=100))

#s = log_drum(note)


s = note_list_to_sound(note_list, log_drum)
s = gain(s, 0.3)

play(s)

save(s, "temp.wav")
#"""