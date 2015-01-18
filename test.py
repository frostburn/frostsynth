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
from frostsynth.polysequence import *
from frostsynth.blit import *
from frostsynth.quantize import *
from frostsynth.numeric import *
from frostsynth.sequence import *
from frostsynth.aplayout import play, stereo_play
from frostsynth.waveout import save, stereo_save
from frostsynth.ffi import malloc_copy, precycloid, j0, j1, jn, y0, y1, yn

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


#s = [lissajous13(220 * t, 1 - t, 0) * 0.5 for t in time(2)]





#fm(0.1, 1)

#s = [fm(220 * t, t) * 0.5 for t in time(5)]

#f = StableFundamental(lambda t, x: cub(t + x * cub(t)), 1)

#s = [tanh(cub(220 * t -2 * exp(-t * 5) * cub(220 * t)) * exp(-t) * 2) * 0.5 for t in time(3)]


#f = [100 + 40 * t for t in time(5)]

#s = list(formant_gen(f, 1500, 1000))

def _theta(t, q):
    coefs = [q ** n ** 2 for n in range(1, 100)]
    return (1 + 2 * sum(c * cos(two_pi * t * n) for n, c in enumerate(coefs, 1))) / (1 + 2 * sum(coefs))


#s = [formant(220 * t, 4, t * 2) * 0.5 for t in time(5)]

#s = [theta_formant(220 * t, t, 10) * 0.5 for t in time(10)]

#f = [150 - sqrt(2-t) * 50 for t in time(2)]

#s0 = list(formant_gen(f, linspace_t(600, 240, 2), linspace_t(30000, 50000, 2)))
#s1 = list(formant_gen(f, linspace_t(940, 2400, 2), 5000))
#s = mix([s0, s1], [0.5, 0.1])

#print(j0(0))

#s = [(sine(220 * t + sine(110 * t) * exp(-t * 5)) - sine(220 * t)) * 0.25 for t in time(2)]
#s += [(sine(220 * t + formant(110 * t, 2, 5) * exp(-t *5)) - sine(220 * t)) * 0.25 for t in time(2)]


#s = [softarc(220 * t, t - 0.5) for t in time(2)]


#s = [logistic(t * 55, t * 0.25, 5) for t in time(4)]


#s = [sinfold(t * 55, 0.5 + sine(t * 3) * 0.1, t * 0.1, 4) * 0.5 for t in time(10)]

if False:
    def i(note):
        return decax2_env([lissajous23(note.frequency * t, exp(-t*7)) for t in time(1.5)], 1, 0.02, 5)


    s = note_tuples_to_sound(i, [
        (C4, 0.2), E4, G4,
    ])


    s = gain(s, 0.2)

#print ([theta_rect(x, 0.9) for x in linspace(0, 1, 200)])



#print (et3(0.9), elliptic_theta3_q(0.9))

#print([max(abs(sine_formant(t, 1, w)) for t in linspace(0, 1, 100)) for w in linspace(0, 10, 200)])


#s = [cis_sum(220 * t, [0, exp(-t), exp(-2*t), exp(-3*t), exp(-4*t), exp(-5*t)]).imag * 0.2  for t in time(1)]
#s = [sin_sum(220 * t, [exp(-t), exp(-2*t), exp(-3*t), exp(-4*t), exp(-5*t)]) * 0.2 for t in time(1)]

#s = [(sine(220 * t) * exp(-t) + sine(2 * 220 * t) * exp(-2 * t) + sine(3 * 220 * t) * exp(-3 *t) + sine(4*220 * t) * exp(-4*t) + sine(5*220 * t) * exp(-5*t)) * 0.2 for t in time(1)]
#s = [theta_formant_c(220 * t, 10 - t, 1 + t * 20) for t in time(10)]

"""
270 ff
520 pp
790 p
1060 f
2025 mf
2670 f (fast decay)
3580 p
4290 p (fast decay)
11985 p (fast decay)
"""

#s = sinepings([1, 0.05, 0.1, 0.7, 0.5, 0.6, 0.03, 0.04, 0.03], [270, 520, 790, 1060, 2670, 3580, 4290, 11985], [1, 3, 2, 3, 2, 9, 3, 15, 15])
#s = gain(s, 0.2)

#s = s[::-1]


#f = lambda x, t=0: sin_sum(x, [0.1, 0.2, 0.5 * sine(t * 2), 1 / (t + 1), 0.5, 0.1])


if False:
    def i(note):
        tp = timed(note.get_phase_gen(), stop=3)
        return [cheb_sum(softarc(p, exp(-t)), [0, exp(-t), exp(-2 * t)  * cub(2 * p + 3 * t), -0.5 * exp(-3 * t), 0.5 * exp(-4 * t)]) for t, p in tp]
        #return [softsaw(2 * p + t + 0.4 * sin_sum(p - t, [0.5, 0.5 * t, 1, 0.5 * t]) * exp(-t*2), 0.8 * exp(-t*5)) * exp(-3*t) for t, p in tp]

    s = notes_to_sound(i, [
        (A1, 0.2), A2, (G2, 0.4), Fs2, F2, (A1, 0.2), (A1, 0.4), (A2, 0.1), (A1, 0.1), (A1, 0.4)
    ])


    s = gain(s, 0.17)


#print([parc(t) for t in linspace(-0.5, 0.5, 100)])


#s = [((1j * parc(220 * t) + par(220 * t)) * cis(440 * t + 10 * t * t)).real * 0.5  for t in time(2)]

if False:
    pitch = eased_step(center([
        (C4, 1, 0.15), C5, G4, (Gs4, 3), (G4, 1),
        (C4, 1), C5, G4, (Gs4, 2), (G4, 2),
        (C4, 1), C5, G4, (Gs4, 2), (C5, 1), G4,
        (C4, 2), (Cs4, 2), (D4, 2), (Ds4, 2),
        (F4, 1), F5, C5, (Cs5, 3), (C5, 1),
        (F4, 1), F5, C5, (Cs5, 2), C5,
        (C4, 1), C5, G4, (C5, 2), (Gs4, 1), G4,
        (Gs4, 2), (G4), (Ds4, 2), (D4, 1), (B3, 1), (C4, 4)
    ], True), t=tempo_gen(240))

    amplitude = eased_step(center([
        (1, 4, 0.03), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.5),
        (1, 6.5), (0, 0.5),
        (1, 4), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.5),
        (1, 1.1), (0, 1), 1, 0, 1, 0, 1, (0, 0.9),
        (1, 4), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.5),
        (1, 6.5), (0, 0.5),
        (1, 4), (0, 0.5), (1, 0.5), (0, 0.5), (1, 1.0), (0, 0.5),
        (1, 3), (0, 1), (1, 2.5), (0, 0.5), (1, 2), (0, 0.5), (1, 0.5), (0, 1)
    ], True), t=tempo_gen(240))

    amplitude = repeat_last(amplitude)

    frequency = [mtof(p) for p in pitch]
    phase = integrate(frequency)

    s = [triangle_octave_sum(p, [1, -1, 0.5, -0.5, 0.1, -0.1]) * a for p, a in zip(phase, amplitude)]
    s = gain(s, 0.25)

#set_srate(44100 * 4)

#s = [softsaw(220 * t, exp(-t*2)) * 0.5 for t in time(5)]
if False:
    ls = LinearSequence.from_flat_list([0,0,80,0,86,5,160,5,167,9,240,9,246,12,660,12])
    ls.scale_x(1 / 160)
    cs = CubicSequence.from_flat_bezier([240,0,373.6666666666667,0.08,507.33333333333337,0.08333333333333333,641,0.9933333333333333])
    cs.scale_x(1 / 160)
    cs.extend_to_zero()
    f = [mtof(C4 + l + c * sine(t * 6)) for t, l, c in timed(ls, cs)]
    s = [cub(p) for p in integrate(f)]

# Song
# First part
s1 = []
if False:
    ls = LinearSequence.from_flat_list([0,-3,80,-3,85,4,120,4,124,0,160,0,165,-1,240,-1,246,-3,320,-3,326,-1,400,-1,406,0,480,0,480,-3,560,-3,563,4,600,4,605,0,640,0,644,-1,720,-1,725,-3,800,-3,805,-1,880,-1,885,7,960,7])
    ls1 = LinearSequence.from_flat_list([0,-3,80,-3,85,4,120,4,124,0,160,0,165,-1,240,-1,246,-3,320,-3,326,-1,400,-1,406,0,480,0,486,-1,960,-1])
    ls.extend(ls1)
    ls.scale_x(1 / 240)

    a_ls = LinearSequence.from_flat_list([0, 0, 7, 1, 960, 1])
    a_ls1 = LinearSequence.from_flat_list([0,1,560,1,568,0,638,0,641,1,760,1,768,0,960,0])
    a_ls.extend(a_ls1)
    a_ls.scale_x(1 / 240)

    f = (mtof(C4 + p) for p in ls)
    s1 = [cheb_sum(duplexn(cub, p, sine(t * 3) * 0.05 + 0.55), [-0.6, 1, -0.5, 0.2, 0.1, -0.05, -0.03])  * 0.2 * a for t, p, a in timed(integrate(f), a_ls)]

# Second part
if False:
    ls = LinearSequence.from_flat_list([0,4,240,4,240,2,400,2,400,4,480,4])
    ls1 = LinearSequence.from_flat_list([0,4,240,4,240,5,398,5,400,4,480,4])
    ls2 = LinearSequence.from_flat_list([0,4,240,4,240,2,320,2,324,0,400,0,403,2,480,2,485,-1,960,-1])
    ls.extend(ls1)
    ls.extend(ls2)
    ls.scale_x(1 / 240)

    a_ls = LinearSequence.from_flat_list([0,0,80,0,85,1,140,1,144,0,160,0,163,1,220,1,225,0,240,0,243,1,300,1,303,0,320,0,323,1,380,1,384,0,400,0,403,1,460,1,464,0,480,0])
    a_ls.extend(a_ls)
    a_ls1 = LinearSequence.from_flat_list([0,0,80,0,85,1,140,1,144,0,160,0,163,1,220,1,225,0,240,0,243,1,620,1,625,0,640,0,644,1,760,1,783,0,960,0])
    a_ls.extend(a_ls1)
    a_ls.scale_x(1 / 240)

    f = (mtof(C4 + p) for p in ls)
    s = [cheb_sum(duplexn(cub, p, sine(t * 3) * 0.07 + 0.6), [-0.6, 1, 0.5, 0.2, 0.1, -0.05, -0.03]) * 0.2 * a for t, p, a in timed(integrate(f), a_ls)]

    ls = LinearSequence.from_flat_list([0,0,240,0,240,-1,400,-1,400,0,480,0])
    ls1 = LinearSequence.from_flat_list([0,0,240,0,240,2,400,2,400,0,480,0])
    ls2 = LinearSequence.from_flat_list([0,0,240,0,240,-1,320,-1,323,-3,400,-3,405,-1,480,-1,485,-5,960,-5])
    ls.extend(ls1)
    ls.extend(ls2)
    ls.scale_x(1 / 240)

    f = (mtof(C4 + p) for p in ls)
    s = add(s, [cheb_sum(duplexn(cub, p, sine(t * 3) * 0.07 + 0.6), [-0.6, 1, 0.5, 0.2, 0.1, -0.05, -0.03]) * 0.2 * a for t, p, a in timed(integrate(f), a_ls)])

    ls = LinearSequence.constant(480, A3)
    ls.extend(ls)
    ls.extend(LinearSequence.constant(480, A3))
    ls.extend(LinearSequence.constant(480, G3))
    ls.scale_x(1 / 240)

    a_ls = LinearSequence.from_flat_list([0,0,4,1,480,0])
    a_ls.extend(a_ls)
    a_ls.extend(LinearSequence.from_flat_list([0,0,4,1,480,0,484,1,640,0.4666666666666667,644,1,960,0]))
    a_ls.scale_x(1 / 240)

    f = (mtof(p) for p in ls)
    s = add(s, [cheb_sum(duplexn(cub, p, sine(t * 3) * 0.07 + 0.6), [-0.6, 1, 0.5, 0.2, 0.1, -0.05, -0.03]) * 0.2 * a for t, p, a in timed(integrate(f), a_ls)])

    s = gain(s, 0.6)

    s = s1 + s

#s = spline_snow_gen([1000 for t in time(2)], variability=0.9)

ns = NaturalSpline([(0, 0), (1, 1), (1.5, 0.5), (2, -1), (3.5, 0)])
ns.differentiate()
ns.differentiate()


s = gain(ns, 0.125)

if True:
    s = dither(s)

    print(max(s),min(s))

    play(s)

    save(s, "temp.wav")
