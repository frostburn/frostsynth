from itertools import *
from math import *
from random import *
from cmath import exp as cexp, log as clog
import cmath

from frostsynth import *
from frostsynth.fft import *
from frostsynth.waveform import *
from frostsynth.instrument import *
from frostsynth.analysis import *
from frostsynth.series import *
from frostsynth.osc import *
from frostsynth.filters import *
from frostsynth.noise import *
from frostsynth.additive import *
from frostsynth.envelope import *
from frostsynth.track import *
from frostsynth.resample import *
from frostsynth.polytable import *
from frostsynth.blit import *
from frostsynth.quantize import *
from frostsynth.aplayout import play, stereo_play
from frostsynth.waveout import save, stereo_save
from frostsynth.ffi import malloc_copy

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

note = Note(pitch=C4, note_on_velocity=0.6, duration=1.0, note_off_velocity=0.3)

perc = Percussion(velocity=0.787401574803)


#beat = 0.1




#s = [sine(220 * t)*0.5 for t in time(2)]


#s = reverb(s)


def wf(phase, sharpness):
    z = from_polar(sharpness, two_pi * phase)
    return cmath.sin(z).imag
    z1 = 1 - z
    return (-clog(z1) + 0.3 * z ** 2 / z1 - 0.1 * z ** 7 / (1.1 - z) ** 2).imag

#s = [wf(t * 100 - t * t + cub(t * 50 - t * t * 2) * (1 - exp(-t)), 0.6 + 0.3 * sine(t * t))  for t in time(5)]

#s = [softtriangle(t * 100 - t * t + softsquare(t * 51 - 3 * t*t, 0.9 - t * 0.2) * (0.5 + 0.4 *sine(t)), 0.9) for t in time(3)]

#s = [sine(s) for s in twozero(s, 1, 1, -2, 1)]
if False:
    windows = []
    window = [cunit() * uniform(None, 0.4, 1) for i in range(100)]
    for s in linspace(0, 1, 10):
        norm = sum(i ** -(1.5 - s) for i in range(1, 100))
        windows.append([b * i ** -(1.5 - s) / norm if i > 0 else 0.0 for i, b in enumerate(window)])

    wf = irfft_waveform2(windows)

    wfm = lambda p, s, m, t: wf(p + cub(2 * p + t) * m, s)

    beat = 0.1

    pitch = eased_step_gen([(E1, 0), (C1, 16 * beat, 8 * beat), (G1, 8 * beat, 4 * beat), (Ef1, 8 * beat, 1 * beat), (C1, 8 * beat, 1 * beat)])
    p = integrate(map(mtof, pitch))
    s = eased_step([(0, 0), (1, 8 * beat, 8 * beat), (0, 8 * beat, 8 * beat)] + [(0.3, 2 * beat, 2 * beat), (0.9, 2 * beat, 2 * beat)] * 16)
    m = eased_step([(0, 0), (1, 8 * beat, 8 * beat), (0, 8 * beat, 8 * beat)] + [(1.0, 32 * beat, 32 * beat)])

    #s = [wfm(p, s, m, t) * 0.2 for p, s, m, t in zip(p, s, m, time_gen())]

    left = [wfm(p, s, m, t) * 0.2 for p, s, m, t in zip(p, s, m, time_gen())]
    right = [wfm(p, s, m, -t) * 0.2 for p, s, m, t in zip(p, s, m, time_gen())]

#left = [wfm(t * 50 - t * t, 0.9 - exp(-t * 2) * 0.2, t * (t-2) * 2, t) for t in time(2)]
#right = [wfm(t * 50 - t * t, 0.9 - exp(-t * 2) * 0.2, t * (t-2) * 2, -t) for t in time(2)]

#from songs.intro import *

#left = [wf(t * 50 - t*t+ cub(101 * t - t*t) * t * (t-2) * 2, 0.9 - exp(-t * 2) * 0.2) * 0.5 for t in time(2)]
#right = [wf(t * 50 - t*t+ cub(99 * t - t*t) * t * (t-2) * 2, 0.9 - exp(-t * 2) * 0.2) * 0.5 for t in time(2)]


if False:
    beat = 0.1
    p = [(kick, beat * 4, 0.7), (hard_snare, beat * 6), (kick, beat * 2), (hard_snare, beat * 4)] * 4

    s = percussion_sequence_to_sound(p)


#def noisy_sof
# gain(mix(map(saw, phase) for phase in noisy_phases(frequency, spread, noise_spread, noise_speed, count)), 0.4 / sqrt(count))

#s = mix(noisy_saw(constant_t(mtof(p), 1)) for p in [C4, E4, G4, C5])

#T = time(3)
#s = mix(mix([softsquare2(p, rsine(t, 5.0, 20.0), rcosine(t * 2, 0.5, 0.7)) * 0.03 for t, p in zip(T, phase)] for phase in noisy_phases_gen(mtof(pitch))) for pitch in [C4, E4, G4, C5])

#s = [twine(t * 220) * 0.5 for t in time(1)]


def arc(phase):
    x = phase - floor(phase + 0.5)
    return cos(2 * asin(x + x))



s = [twine(t * 220) * 0.5 for t in time(1)]

s = [saw(t * 220) * 0.5 for t in time(1)] + s + [par(t * 220) * 0.5 for t in time(1)]

#s = differentiate(s)

#s = gain(s, 0.2)

#s = [triangle(qua(t * 40) * theta_rect(t, 0.7) + qua(t * 40 * 5) * theta_rect(t + 0.3, 0.7) + cub(t * 40 * 7) * theta_rect(t + 0.6, 0.9) + t * 40, 0.5 + 0.1 * t) * 0.5 for t in time(5)]

#s = differentiate(s)


#note.frequency = mtof(A3)
#print(note.frequency)
#s = flute(note)

s = dither(s)

play(s)

save(s, "temp.wav")



#print (stereo_mix([([0,0], [1,2]), ([3, 4], [5, 6])]))

#import frostsynth.songs.intro
#left = timeslice(comb_t(s, 2 * beat - 0.02, 0.51), 128 * beat)
#right = timeslice(comb_t(s, 2 * beat + 0.02, 0.5), 128 * beat)

#stereo_play(left, right)
#stereo_save(left, right, "temp.wav")