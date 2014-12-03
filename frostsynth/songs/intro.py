from itertools import *
from math import *
from random import *
from cmath import exp as cexp, log as clog

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
from frostsynth.aplayout import play, stereo_play
from frostsynth.waveout import save, stereo_save
from frostsynth.ffi import malloc_copy


# Intro
beat = 0.1
pitch = eased_step_gen(cycle([(C3, 3 * beat, 0.02), (D3, beat), (G3, 2 * beat), (A3, 2 * beat)]))
transpose = eased_step_gen(cycle([(unison, beat * 32, 0.02), (fifth, beat * 32)]))
f = map(mtof, add_gen(pitch, transpose))
p = integrate_gen(f)
s = (0.25 * softsquare(p, 1 - exp(-t * 0.5)) for t, p in zip(time_gen(), p))

s = Infinitee(chain(timeslice(s, 128 * beat), zero_t(3)))

left = list(comb_t(s, 2 * beat - 0.02, 0.51))
right = list(comb_t(s, 2 * beat + 0.02, 0.5))

stereo_play(left, right)

stereo_save(left, right, "temp.wav")
