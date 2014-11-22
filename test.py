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
from resample import *
from polytable import *
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

# --------------
note_list = [AbsoluteNote(pitch=A3, note_on_time=0.0, note_on_velocity=0.685039370079, duration=0.119791666667, note_off_velocity=0.787401574803),
 AbsoluteNote(pitch=C4, note_on_time=0.5, note_on_velocity=0.629921259843, duration=0.296875, note_off_velocity=0.362204724409),
 AbsoluteNote(pitch=D4, note_on_time=1.0, note_on_velocity=0.496062992126, duration=0.125, note_off_velocity=0.370078740157),
 AbsoluteNote(pitch=Eb4, note_on_time=1.125, note_on_velocity=0.511811023622, duration=0.0989583333333, note_off_velocity=0.527559055118),
 AbsoluteNote(pitch=D4, note_on_time=1.375, note_on_velocity=0.708661417323, duration=0.3359375, note_off_velocity=0.314960629921),
 AbsoluteNote(pitch=C4, note_on_time=1.75, note_on_velocity=0.472440944882, duration=0.166666666667, note_off_velocity=0.259842519685),
 AbsoluteNote(pitch=A3, note_on_time=2.0, note_on_velocity=0.582677165354, duration=0.1484375, note_off_velocity=0.307086614173),
 AbsoluteNote(pitch=A4, note_on_time=2.25, note_on_velocity=0.385826771654, duration=0.114583333333, note_off_velocity=0.259842519685),
 AbsoluteNote(pitch=A4, note_on_time=2.5, note_on_velocity=0.51968503937, duration=0.153645833333, note_off_velocity=0.354330708661),
 AbsoluteNote(pitch=A4, note_on_time=2.75, note_on_velocity=0.582677165354, duration=0.125, note_off_velocity=0.354330708661),
 AbsoluteNote(pitch=G4, note_on_time=3.0, note_on_velocity=0.629921259843, duration=0.231770833333, note_off_velocity=0.181102362205),
 AbsoluteNote(pitch=E4, note_on_time=3.375, note_on_velocity=0.629921259843, duration=0.270833333333, note_off_velocity=0.338582677165),
 AbsoluteNote(pitch=D4, note_on_time=3.75, note_on_velocity=0.59842519685, duration=0.158854166667, note_off_velocity=0.370078740157),
 AbsoluteNote(pitch=A3, note_on_time=4.0, note_on_velocity=0.551181102362, duration=0.182291666667, note_off_velocity=0.299212598425),
 AbsoluteNote(pitch=C4, note_on_time=4.5, note_on_velocity=0.527559055118, duration=0.166666666667, note_off_velocity=0.338582677165),
 AbsoluteNote(pitch=D4, note_on_time=5.0, note_on_velocity=0.464566929134, duration=0.127604166667, note_off_velocity=0.346456692913),
 AbsoluteNote(pitch=Eb4, note_on_time=5.125, note_on_velocity=0.692913385827, duration=0.1015625, note_off_velocity=0.283464566929),
 AbsoluteNote(pitch=D4, note_on_time=5.375, note_on_velocity=0.629921259843, duration=0.171875, note_off_velocity=0.307086614173),
 AbsoluteNote(pitch=C4, note_on_time=5.75, note_on_velocity=0.661417322835, duration=0.135416666667, note_off_velocity=0.370078740157),
 AbsoluteNote(pitch=A3, note_on_time=6.0, note_on_velocity=0.511811023622, duration=0.182291666667, note_off_velocity=0.291338582677),
 AbsoluteNote(pitch=G3, note_on_time=6.25, note_on_velocity=0.535433070866, duration=0.145833333333, note_off_velocity=0.228346456693),
 AbsoluteNote(pitch=E3, note_on_time=6.75, note_on_velocity=0.488188976378, duration=1.03385416667, note_off_velocity=0.48031496063)]

bass_list = [AbsoluteNote(pitch=A1, note_on_time=0.0, note_on_velocity=0.606299212598, duration=0.119791666667, note_off_velocity=0.787401574803),
 AbsoluteNote(pitch=C2, note_on_time=0.5, note_on_velocity=0.59842519685, duration=0.119791666667, note_off_velocity=0.787401574803),
 AbsoluteNote(pitch=D2, note_on_time=1.0, note_on_velocity=0.590551181102, duration=0.119791666667, note_off_velocity=0.787401574803),
 AbsoluteNote(pitch=Eb2, note_on_time=1.375, note_on_velocity=0.669291338583, duration=0.119791666667, note_off_velocity=0.787401574803),
 AbsoluteNote(pitch=G1, note_on_time=1.625, note_on_velocity=0.590551181102, duration=0.119791666667, note_off_velocity=0.787401574803)]

percussion_list = [AbsolutePercussion(index=36, note_on_time=0.0, velocity=0.614173228346),
 AbsolutePercussion(index=42, note_on_time=0.25, velocity=0.787401574803),
 AbsolutePercussion(index=38, note_on_time=0.5, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=0.75, velocity=0.787401574803),
 AbsolutePercussion(index=35, note_on_time=1.0, velocity=0.614173228346),
 AbsolutePercussion(index=42, note_on_time=1.25, velocity=0.787401574803),
 AbsolutePercussion(index=38, note_on_time=1.5, velocity=0.787401574803),
 AbsolutePercussion(index=42, note_on_time=1.75, velocity=0.787401574803)]
"""
s = note_list_to_sound(loop(note_list, 2, 8.0), organ)

s = gain(s, 0.5)

b = note_list_to_sound(loop(bass_list, 8, 2.0), bass)

b = gain(b, 0.5)

p = percussion_list_to_sound(loop(percussion_list, 8, 2.0), percussion_bank)

p = gain(p, 0.5)

s = merge(merge(s, p, 0), b, 0)

s = list(reverb(s))
"""
#s = softsaw_bass(AbsoluteNote(pitch=E4, note_on_time=0.0, note_on_velocity=0.566929133858, duration=0.525, note_off_velocity=0.0))

#print(s)

#perc = Percussion(velocity=0.787401574803)

#s = gain(snare(perc) + zero(2), 0.7)

#s = schroeder_t(s, 0.01, 0.4)

#s = schroeder_t(s, 0.017, 0.3)



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


#s = note_list_to_sound(note_list, log_drum)
#s = gain(s, 0.3)

def train_g():
    window, dt = train_window()
    result = []
    for f in window:
        x = (f - 1000) / 20000.0
        result.append(0.0001 * exp(-100 * x**2) * cexp(two_pi * random()))
    result_even = []
    for i in range(len(result)):
        result_even.append(-(-1) ** i * result[i])
    while True:
        yield result
        yield result_even

#s = list(timeslice(process_window_train(train_g()), 1))

#w = [0.5 * cunit() * cosine(f / 1000.0) ** 64 * (500.0 / (f + 1)) ** 2 * (f > 400) for f in freq_window(1 << 16)]

#w = [10 * cunit() * (exp(-0.01 * (f - 500) ** 2) + exp(-0.01 * (f - 1000) ** 2) + exp(-0.01 * (f - 2000) ** 2)) for f in freq_window(1 << 16)]

#w = [10 * cunit() * exp(-200 * sin(pi * f / freq) ** 2) * (2 * f > freq) * ((f + 0.01) / freq) ** -1 for f in freq_window(1 << 16)]


#s *= 2

srate = get_srate()

"""
result = []
bandwith = 30.0
freq = 440.0
snows = [snow1_gen(repeat(bandwith), vmin=-1.0, vmax=1.0, variability=1.0) for i in range(5 * 3 + 2)]
for t in time(1):
    s = 0.0
    for e in range(5):
        phase = freq * t
        p = sine(phase * 2 ** e) * next(snows[3 * e])
        p += sine(phase * 3 ** e) * 0.8 / (e + 1) * next(snows[3 * e + 1])
        p += sine(phase * 5 ** e) * 0.4 / (e + 1) * next(snows[3 * e + 2])
        if e > 3:
            p /= (e - 3) ** 2
        s += p
    s += sine(phase * 6 * freq) * 0.5 * next(snows[-2])
    s += sine(phase * 10 * freq) * 0.2 * next(snows[-1])
    result.append(0.1 * s)
"""
"""
result = []
for t in time(1):
    s = 0.0
    m = 1.0
    for e in range(6):
        s += sine(t * 220 * m)
        m *= 2 ** (12 / 12)
    result.append(s * 0.1)



#s = [pen(440 * t) * n for t, n in zip(time(2), snow1_gen(repeat(40), vmin=0.1, vmax=1.0, variability=1.0))]

s = result
"""
"""
s = []
buf = [0.0] * 300
buf1 = [0.0] * 301
buf2 = [0.0] * 302
y0 = 0.0
y0_1 = 0.0
y0_2 = 0.0
x1 = 0.0
x1_1 = 0.0
x1_2 = 0.0
for j in range(int(2 * srate)):
    i = j % len(buf)
    i1 = j % len(buf1)
    i2 = j % len(buf2)
    s.append(0.1 * buf[i] + 0.1 * buf1[i1] + 0.1 * buf2[i2])
    y0 = y0 * 0.845 - buf[i] * 0.8 + x1 * 0.95 + exp(-0.1 * (j-10)**2) + 0.0 * buf2[i2]
    x1 = buf[i]
    y0_1 = y0_1 * 0.505 - buf1[i1] * 0.5 + x1_1 * 0.95 + exp(-0.1 * (j-20)**2) + 0.0 * buf[i]
    x1_1 = buf1[i1]
    y0_2 = y0_2 * 0.005 - buf2[i2] * 0.05 + x1_2 * 0.95 + exp(-0.1 * (j-30)**2) + 0.0 * buf1[i1]
    x1_2 = buf2[i2]
    buf[i] = y0
    buf1[i1] = y0_1
    buf2[i2] = y0_2
"""

"""
for i in range(12):
freq = 100

buf = [0.0] * int(srate / (2.05 * freq))
buf1 = [0.0] * int(srate / (3.05 * freq))
s = []
y0 = 0.0
y0_1 = 0.0
for j in range(int(1 * srate)):
    t = j / srate
    i = j % len(buf)
    i1 = j % len(buf1)
    e0 = duplex(par, freq * j / srate, 0.55) * exp(-1 * t)
    e = e0 * sine(3 * t)
    y0 = y0 * 0.2 + buf[i] * 0.77 + e * 0.05
    y0_1 = y0_1 * 0.2 + buf1[i1] * 0.77 + e * 0.06
    buf[i] = y0
    buf1[i1] = y0_1
    temp = y0 * e + 2 * y0_1 + 0.05 * e + 0.2 * e0
    s.append(0.5 * temp)

"""

#srate = set_srate(srate * 2)
"""
T = 60

phase = integrate((int("36364689"[k>>13&7])&15) * 50 for k in range_t(T))
s0 = [0.5 * duplex(par, p) for p in phase]

phase = integrate((((k>>12)^(k>>12)-2)%11) * 100 for k in range_t(T))
bias = [(k >> 13 & 127) / 256 + 0.1 for k in range_t(T)]
s1 = [0.5 * duplex(par, p, b) for p, b in zip(phase, bias)]

s = gain(mix([s0, s1]), 0.5)
"""

"""
s = [0.5 * tanh((cis(105 * t) * constant_series(cis(150 * t + 10 * t * t + cub(456 * t) * 0.2) * (0.7 + 0.25 * sine(3 * t)))).imag * par(2 * t)) for t in time(5)]
s = list(comb_t(s, 0.5, 0.5))

train = fft_train(s, include_time=True)

def train_g():
    for t, w in train:
        yield [2 * b * (0.2 + exp(-0.0001 * (f - t * 200 - 200 - t * t * 20)**2) + exp(-0.0001 * (f - t * 300 - 1000)**2)) for f, b in freq_enumerate(w)]

s = ifft_train(train_g())
"""

"""
freq = 220

freqs = [k * freq for k in range(1, 20)]

for e in range(14, 16):
    window_size = (1 << e)
    df = srate / window_size
    freqs_appr = [round(f / df) * df for f in freqs]
    print(freqs_appr)
    window = [0.0] * (window_size // 2 + 1)
    for f in freqs:
        window[int(round(f / df))] = 0.1 * 220.0 / f
    #window[int(round(220 / df))] = 1.0j
    s = pseudo_irfft(window)
    s = timeslice(cycle(s), 1)
"""

"""
s = []
buf = [0.0] * 400
y0 = 0.0
x0 = 0.0
y0_1 = 0.0
x0_1 = 0.0
for k in range_t(3):
    g = -0.99
    i = k % len(buf)
    x1 = x0
    x0 = buf[i] + 0.5 * exp(-0.001 * (k - 1000) ** 2)
    y0 = -g * y0 + g * x0 + x1
    x1_1 = x0_1
    x0_1 = y0
    y0_1 = -g * y0_1 + g * x0_1 + x1_1
    buf[i] = y0_1 * 0.9 - y0 * 0.09
    s.append(y0)
"""

#track = [(C4, 0.05, 0.0), (E4, 0.05, 0.0), C5, E5, G4]
#phase = integrate_gen(map(mtof, eased_step_gen(cycle(track))))

#wf = lambda p: softsquare(p*3, sine(p * 0.02))
#s = list(map(wf, timeslice(phase, 5)))

#n = uniform(200)
#st = LinearTable(n, True)

#s = [0.2 * st(200 * t * 35) for t in time(2)]


# Wub base
track = [(A2, 0.5, 0.1), C3, Ds3, Es3, E3]
phase = integrate_gen(map(mtof, eased_step_gen(cycle(track))))
phase = gain_gen(phase, 0.3)

n = uniform(500)
st = LinearTable(n, True)
wf = lambda p: st(len(n) * p)

s = [wf(p) for p in timeslice(phase, 10)]

train = fft_train(s, include_time=True)

def train_g():
    for t, w in train:
        yield [2 * b * (0.2 + exp(-0.0001 * (f - t * 100 - 50)**2) + exp(-0.0001 * (f - t * 100 - 200)**2)) * exp(-0.0001 * f / (1.01 + softsquare(2 * t, 0.9))) for f, b in freq_enumerate(w)]

s = ifft_train(train_g())
s = gain(s, 0.1)

play(s)

save(s, "temp.wav")
