from math import log
from base import *


def step_sequence_gen(track, click=False, fillvalue=0.0, t=None, srate=None):
    """Turns list of (value, duration) tuples into a generator that outputs each value for the given duration (defaults to the previous duration or 1). If click is True it emits values only once and fillvalue the rest of the time. Optionally driven by a time generator t which defaults to time in seconds."""
    if t is None:
        t = timegen(srate=srate)
    else:
        t = iter(t)
    t0 = next(t)
    t1 = t0
    dur = 1
    for tple in track:
        if hasattr(tple,'__getitem__'):
            value = tple[0]
            if len(tple) > 1:
                dur = tple[1]
        else:
            value = tple
        while t0 + dur > t1:
            yield value
            if click:
                value = fillvalue
            t1 = next(t)
        t0 = t1


def mtof(p):
    """Converts midi pitch to frequency."""
    return 440.0 * 2 ** ((p - 69) / 12.0)


def ftom(f):
    """Converts frequency to midi pitch."""
    return 69 + 12 * log(f / 440.0, 2)





class Rest:
    pass


#Spam the International names of midi pitches into the namespace.
for octave in range(10):
    for i, key in enumerate(["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]):
        exec(key + str(octave) + "=" + str(12 * (octave + 1) + i))
    for i, key in [(-1, "Cb"), (1, "Cs"), (3, "Ds"), (5, "Es"), (4, "Fb"), (6, "Fs"), (8, "Gs"), (10, "As"), (12, "Bs")]:
        exec( key + str(octave) + " = " + str(12 * (octave + 1) + i))
