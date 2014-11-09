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

note_list = [
    AbsoluteNote(pitch=E4, note_on_time=0.0, note_on_velocity=0.566929133858, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=0.0, note_on_velocity=0.551181102362, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=0.581818181818, note_on_velocity=0.566929133858, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=C4, note_on_time=1.16363636364, note_on_velocity=0.55905511811, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=1.74545454545, note_on_velocity=0.622047244094, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=2.32727272727, note_on_velocity=0.669291338583, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=2.32727272727, note_on_velocity=0.622047244094, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=2.90909090909, note_on_velocity=0.614173228346, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=3.49090909091, note_on_velocity=0.582677165354, duration=1.05, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=4.65454545455, note_on_velocity=0.590551181102, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=4.65454545455, note_on_velocity=0.606299212598, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=5.23636363636, note_on_velocity=0.606299212598, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=5.81818181818, note_on_velocity=0.590551181102, duration=1.05, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=6.98181818182, note_on_velocity=0.645669291339, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=6.98181818182, note_on_velocity=0.622047244094, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=G4, note_on_time=7.56363636364, note_on_velocity=0.661417322835, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G4, note_on_time=8.14545454545, note_on_velocity=0.590551181102, duration=1.05, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=9.30909090909, note_on_velocity=0.574803149606, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=9.30909090909, note_on_velocity=0.614173228346, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=9.89090909091, note_on_velocity=0.543307086614, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=C4, note_on_time=10.4727272727, note_on_velocity=0.55905511811, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=11.0545454545, note_on_velocity=0.629921259843, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=11.6363636364, note_on_velocity=0.661417322835, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=11.6363636364, note_on_velocity=0.622047244094, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=12.2181818182, note_on_velocity=0.59842519685, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=12.8, note_on_velocity=0.582677165354, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=13.3818181818, note_on_velocity=0.606299212598, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=13.9636363636, note_on_velocity=0.590551181102, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=G3, note_on_time=13.9636363636, note_on_velocity=0.614173228346, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=14.5454545455, note_on_velocity=0.582677165354, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=E4, note_on_time=15.1272727273, note_on_velocity=0.637795275591, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=D4, note_on_time=15.7090909091, note_on_velocity=0.551181102362, duration=0.525, note_off_velocity=0.0),
    AbsoluteNote(pitch=C4, note_on_time=16.2909090909, note_on_velocity=0.574803149606, duration=2.21363636364, note_off_velocity=0.0),
    AbsoluteNote(pitch=E3, note_on_time=16.2909090909, note_on_velocity=0.566929133858, duration=2.21363636364, note_off_velocity=0.0)
]

s = note_list_to_sound(note_list, softsaw_bass)

s = gain(s, 0.5)

#s = softsaw_bass(AbsoluteNote(pitch=E4, note_on_time=0.0, note_on_velocity=0.566929133858, duration=0.525, note_off_velocity=0.0))

#print(s)

#s = snare()

play(s)

save(s, "temp.wav")
#"""