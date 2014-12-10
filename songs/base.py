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
