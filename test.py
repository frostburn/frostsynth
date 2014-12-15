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
from frostsynth.ffi import malloc_copy, precycloid

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


if False:
    sharpness = xfader(center([
        ((rsine(t - 0.1 - cub(t - 0.1) * 0.5, 0.8, 1 - exp(-t) * 0.1) for t in time_gen()), 2.0, 0.1),
        (0.99, 2.0),
        ((rsine(t - 0.1 - cub(t - 0.1) * 0.5, 0.5, 1 - exp(-t) * 0.05) for t in time_gen()), 2.0),
        (0.99, 2.0),
    ]))

    modulation = linspace_t(0, 1, 8)

    pitch = eased_step(center([
        (A2, 2, 0.1), (A3, 1.5), (A2, 0.5), (As2, 2), (C3, 1.5), (As2, 0.5),
    ], True))

    frequency = [mtof(p) for p in pitch]

    channels = []
    for sign in [-1, 1]:
        ss = []
        for phase in noisy_phases(frequency, 0.25, 0.5):
            ss.append([softsaw(p + cub(2 * p + t * sign) * m, s) * 0.1 for t, p, s, m in timed(phase, sharpness, modulation)])
        s = mix(ss)
        channels.append(s)

    left, right = channels

    stereo_play(left, right)
    stereo_save(left, right, "temp.wav")






s = [lissajous11(t * 220, 1 - t) * 0.5 for t in time(2)]

#print(max(s),min(s))

s = dither(s)

play(s)

save(s, "temp.wav")
