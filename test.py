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
from blit import *
from aplayout import play
import wavein
from waveout import save
from ffi import malloc_copy

srate = get_srate()

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

perc = Percussion(velocity=0.787401574803)
"""
def convolve(source, kernel, mode="tail"):
    if mode != "tail":
        raise ValueError("Only tail mode implemented")
    kernel = kernel[::-1]
    l = len(kernel)
    buf = [0.0] * (len(source) + l - 1)
    for i in range(l)):
        buf[i] = sum(s * k for s, k in zip(source, kernel[-i - 1:])
    for i in range(len(source)):
        buf[i + l] = sum(s * k for s, k in zip(source[i + 1:len], kernel))
"""
"""
with Srate(srate * 8):
    s = [0.5 * cub(t * 1000 + cub(t * 3000) * exp(-5 * t)) * exp(-3 * t) for t in time(1)]

    s += [0.5 * cub(t * 1500 + cub(t * 4000) * exp(-5 * t)) * exp(-3 * t) for t in time(2)]

    s = list(lpf(lpf(s, 40000), 40000))[::8]

kernel = [0.01 * n for i, n in enumerate(fast_uniform(2000))]

s = list(comb(convolve_list(s, kernel), 2001, 0.7))
#s = list(convolve(s, kernel))


"""
"""
def r(s, frequency=0.025, Q=10):
    def g(frequency):
        i = 0
        while True:
            i += 1
            if i == 200:
                frequency /= 2
            w0 = 2.0 * pi * frequency
            cosw0 = cos(w0)
            alpha = sin(w0) / (2.0 * Q)
            yield (1.0 + alpha, -2.0 * cosw0, 1.0 - alpha, 1, 0, 0)

    return dynamic_biquad(s, g(frequency))


def res(s, frequency=0.025, decay=0.25):
    y0 = 0j
    for i, sample in enumerate(s):
        if i == 200:
            frequency /= 2
        a1 = cexp(-(decay + two_pi_j) * frequency)
        y0 = 1j * sample + a1 * y0
        yield y0.real




s = [1] + [0] * 400

s = list(r(s))

print(s)
"""

#s = fast_uniform_t(5)
#s0 = s
#f = [1 + t * 4410 for t in time(5)]

#s = gain(dynamic_bpf0(s, f, repeat(0.6)), 0.1)
#s = gain(dynamic_bandpass(s, f, repeat(10)), 0.1)

#s = mix([s, s0])

#s = gain(s, 0.1)

#s = malloc_copy(8, 5000)
#set_srate(22050)

"""
phase = integrate_gen(map(mtof, eased_step_gen(cycle([(C4, 0.2, 0.05), E4, G4]))))
amplitude = eased_step_gen(cycle([(1, 0.15, 0.01), (0, 0.05, 0.02)]))

s = [(saw(p) + saw(p + 2 * t)) * 0.5 * a for t, p, a in zip(time(3), phase, amplitude)]

#n = gain(uniform(200), 0.05)

ks = ([0.01 * sin((2000 + T * 200) * t + 7 * sin((5000 - T * 1000) * t)) for t in time(0.05)] for T in time_dt_gen(0.01))

s = dynamic_convolve(s, ks, dt=0.01)

#s = comb(s, 500, 0.9)

#s = reverb(s)

s = gain(s, 0.5)
"""

#s = list(bpf0([1] + [0] * 10000, 11025, 1))
#s /= max(s)
"""
from cmath import sqrt as csqrt

def dynamic_resonator(source, frequency, Q, srate=None):
    srate = get_srate(srate)
    dt = 1.0 / srate
    y0 = 0.0j
    for sample, f, q in zip(source, frequency, Q):
        w0 = two_pi * f * dt
        cosw0 = cos(w0)
        alpha = sin(w0) / (2.0 * q)
        a1 = (cosw0 + csqrt(alpha ** 2 + cosw0 ** 2 - 1.0)) / (1 + alpha)
        y0 = 1j * sample + a1 * y0
        yield y0.real
"""

def quadratic_onepole(source, a, b, aa, ab, bb):
    y = 0
    for sample in source:
        y = b * sample + a * y + bb * sample ** 2 + ab * sample * y + aa * y ** 2
        yield y


#s = [cub(t * 220 + t * t * 10) + par(t * 330 + t * t * 10) for t in time(2)]
#s0 = s
#f = [1 + t * 4400 for t in time(5)]

#s = gain(quadratic_onepole(s, -0.3, 0.9, 0, -0.5, 0), 0.05)

"""
s = zero_t(2)
for i in range(0, 12 * 2):
    f = 110 * 2 ** (i / 12)
    p = [cub(t * f + 0.4 * cub(t * f * 3) * exp(-6 * t)) * exp(-3 * t) for t in time(2)]
    s = add(s, p)

k = gain(s, 0.0002)

f = 220
s = [cub(t * f + 0.4 * cub(t * f * 3) * exp(-6 * t)) * exp(-3 * t) for t in time(2)]

s = add(convolve(s, k), s)

s = gain(s, 0.1)
"""

#s = []
#for f in [220, 220 * 1.5, 440]:
#    s += [cub(t * f + 0.4 * cub(t * f * 6 + n) * exp(-6 * t) + 2 * t * cub(t * f - n) * exp(-5 * t)) * exp(-3 * t) for t, n in zip(time(2), snow3_gen(f * 0.01))]

#s = gain(mix([s, grand(s)], [5, 1]), 0.005)

#s = gain(list(reverb(s)), 0.4)

#s = impulse(1000)

#d = 0.6
#g = 1.0

#s = list(onepole(s, 1, -d, g * (1 - d)))

#print(mtof(A2))





#s = [sine(220 * t) * n0 + cosine(220 * t) * n1 for t, n0, n1 in zip(time(10), lpnoise_gen(15, 3), lpnoise_gen(15, 3))]

f = [1.0 + t * 2250 / 5.0  for t in time(5)]

s = [0.1 + t / 5.0 for t in time(5)]



#s = gain(dynamic_bpf0(s, repeat(20000), repeat(10)), 0.5)
#s = gain(dynamic_resonator(s, repeat(1), repeat(20000), repeat(10)), 0.5)

#s = gain(dynamic_lpf(s, repeat(20000), repeat(10.51)), 0.5)

s = gain(sawblit(f, s, 0.5, 0.0), 0.1)

#s = [0.1 * sine_odd_series(t, 10) for t in time(1)]

#s = [0.1 * constant_series_n_mu(cis(t), 1.5).real for t in time(1)]

#play(s)

save(s, "temp.wav")
