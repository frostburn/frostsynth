from itertools import *
from math import *
from random import *
from cmath import exp as cexp

from base import *
from fft import *
from osc import *
from instrument import *
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

f = wavein.open("zelda_whistle.wav")

from cmath import polar

def delta_phi(phi1, phi2):
    delta = phi2 - phi1
    if delta < -pi:
        delta += 2 * pi
    elif delta > pi:
        delta -= 2 * pi
    return delta

def unwrap_phase(phis):
    result = [0.0] * len(phis)
    running_total = 0.0
    inverse_two_pi = 0.5 / pi
    for i in range(len(phis) - 1):
        running_total += delta_phi(phis[i + 1], phis[i]) * inverse_two_pi # Reversed and normalized to get a positive phase signal in the most common use case.
        result[i + 1] = running_total
    return result
    #return list(accumulate(chain([0], starmap(delta_phi, zip(phis, phis[1:])))))

def polar_decomposition(signal):
    """Returns a DC-blocked polar decomposition of a real-valued sinusoidal signal."""
    padded_signal = pad(signal)
    dft = fft(padded_signal)
    half = len(dft) // 2
    dft[:half] = [0.0] * half
    ps = [polar(z) for z in ifft(dft)[:len(signal)]]
    rs, phis = zip(*ps)
    return zip(rs, unwrap_phase(phis))

def sine5(p, r):
    x = p * 2 * pi
    return sin(x + sin(x * 5) * r * 0.5)

s = [r * sine5(p, r) for r, p in polar_decomposition(f)]

play(s)

save(s, "zelda.wav")
