from itertools import *
from math import *
from random import *
from cmath import exp as cexp

from base import *
from fft import *
from osc import *
from instrument import *
from analysis import *
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

s = [0.2 * (par_complement(t * 220) * cos(500 * t * t) - par(t * 220) * sin(500 * t * t)) for t in time(5)]

play(s)

save(s, "temp.wav")
#"""