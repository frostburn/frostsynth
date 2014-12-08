from math import log
from itertools import repeat

from frostsynth import *


def step_sequence_gen(track, click=False, fillvalue=0.0, t=None, srate=None):
    """
    Turns list of (value, duration) tuples into a generator that outputs each value for the given duration (defaults to the previous duration or 1).
    If click is True it emits values only once and fillvalue the rest of the time. Optionally driven by a time generator t which defaults to time in seconds.
    """
    if t is None:
        t = time_gen(srate=srate)
    else:
        t = iter(t)
    t0 = next(t)
    t1 = t0
    duration = 1
    for tple in track:
        if hasattr(tple,'__getitem__'):
            value = tple[0]
            if len(tple) > 1:
                duration = tple[1]
        else:
            value = tple
        while t0 + duration > t1:
            yield value
            if click:
                value = fillvalue
            t1 = next(t)
        t0 = t1


def eased_step_gen(track, t=None, srate=None):
    """
    Turns list of (value, duration, ease_duration) tuples into a generator that outputs each value for the given duration (defaults to the previous duration or 1).
    """
    if t is None:
        t = time_gen(srate=srate)
    else:
        t = iter(t)
    t0 = next(t)
    t1 = t0
    old_value = None
    duration = 1
    ease_duration = 0
    for tple in track:
        if hasattr(tple,'__getitem__'):
            value = tple[0]
            if len(tple) > 1:
                duration = tple[1]
                if len(tple) > 2:
                    ease_duration = min(tple[2], duration)
        else:
            value = tple
        if old_value is None:
            old_value = value
        while t0 + duration > t1:
            local_t = t1 - t0
            if local_t < ease_duration:
                mu = local_t / ease_duration
                yield old_value + mu * (value - old_value)
            else:
                yield value
            t1 = next(t)
        t0 = t1
        old_value = value


def eased_step(track, t=None, srate=None):
    return list(eased_step_gen(track, t, srate))


def mtof(p):
    """Converts midi pitch to frequency."""
    return 440.0 * 2 ** ((p - 69) / 12.0)


def ftom(f):
    """Converts frequency to midi pitch."""
    return 69 + 12 * log(f / 440.0, 2)


# Spam the International names of midi pitches into the namespace.
pitch_names = {}
for octave in range(10):
    for i, key in enumerate(["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]):
        name = key + str(octave)
        value = 12 * (octave + 1) + i
        pitch_names[value] = name
        exec(name + "=" + str(value))
    for i, key in [(-1, "Cb"), (1, "Cs"), (3, "Ds"), (5, "Es"), (4, "Fb"), (6, "Fs"), (8, "Gs"), (10, "As"), (12, "Bs")]:
        exec( key + str(octave) + " = " + str(12 * (octave + 1) + i))
    for i, key in [(-1, "Cf"), (1, "Df"), (3, "Ef"), (4, "Ff"), (6, "Gf"), (8, "Af"), (10, "Bf")]:
        exec( key + str(octave) + " = " + str(12 * (octave + 1) + i))

# Interval names
P1 = dim2 = unison = prime = 0
m2 = Aug1 = minor_second = semitone = 1
M2 = dim3 = major_second = tone = 2
m3 = Aug2 = minor_third = 3
M3 = dim4 = major_third = 4
P4 = Aug3 = fourth = 5
dim5 = Aug4 = tritone = 6
P5 = dim6 = fifth = 7
m6 = Aug5 = minor_sixth = 8
M9 = dim7 = major_sixth = 9
m7 = Aug6 = minor_seventh = 10
M7 = dim8 = major_seventh = 11
P8 = Aug7 = octave = 12


class Event(object):
    def __init__(self, srate=None):
        self._srate = srate

    @property
    def srate(self):
        return get_srate(self._srate)


class Note(Event):
    def __init__(self, pitch=None, frequency=None, note_on_velocity=None, duration=None, note_off_velocity=None, srate=None):
        super().__init__(srate=srate)
        if pitch is not None:
            if frequency is not None:
                raise ValueError("Only pitch or frequency can be supplied.")
            self.frequency = mtof(pitch)
        else:
            if frequency is None:
                raise ValueError("Pitch or frequency must be supplied.")
            self.frequency = frequency
        self.pitch = pitch
        self.note_on_velocity = note_on_velocity
        self.duration = duration
        self.note_off_velocity = note_off_velocity


    def get_frequency_gen(self):
        return repeat(self.frequency)


class AbsoluteMixin(object):
    def __lt__(self, other):
        return self.note_on_time < other.note_on_time

    @property
    def note_on_sample(self):
        return int(self.note_on_time * self.srate)


# TODO: Handle the pitchless case
class AbsoluteNote(Note, AbsoluteMixin):
    def __init__(self, pitch=None, frequency=None, note_on_time=None, note_on_velocity=None, duration=None, note_off_velocity=None, srate=None):
        super().__init__(pitch=pitch, frequency=frequency, note_on_velocity=note_on_velocity, duration=duration, note_off_velocity=note_off_velocity, srate=srate)
        self.note_on_time = note_on_time

    def copy(self, offset=0.0):
        return AbsoluteNote(self.pitch, None, self.note_on_time + offset, self.note_on_velocity, self.duration, self.note_off_velocity, self._srate)

    def __repr__(self):
        if self.pitch:
            return "AbsoluteNote(pitch=%s, note_on_time=%s, note_on_velocity=%s, duration=%s, note_off_velocity=%s)" % (
                pitch_names[self.pitch], self.note_on_time, self.note_on_velocity, self.duration, self.note_off_velocity
            )


class Percussion(Event):
    def __init__(self, velocity=None, srate=None):
        super().__init__(srate=srate)
        self.velocity = velocity


class AbsolutePercussion(Percussion, AbsoluteMixin):
    def __init__(self, index=None, note_on_time=None, velocity=None, srate=None):
        super().__init__(velocity=velocity, srate=srate)
        self.index = index
        self.note_on_time = note_on_time

    def copy(self, offset=0.0):
        return AbsolutePercussion(self.index, self.note_on_time + offset, self.velocity, self.srate)

    def __repr__(self):
        return "AbsolutePercussion(index=%s, note_on_time=%s, velocity=%s" % (self.index, self.note_on_time, self.velocity)


def merge(list1, list2, k):
    result = list1 + [0] * max(0, len(list2) + k - len(list1))
    result[k:(k + len(list2))] = [i1 + i2 for i1, i2 in zip(result[k:], list2)]
    return result


def note_list_to_sound(track, instrument):
    result = []
    for absolute_note in sorted(track):
        instrument_sound = instrument(absolute_note)
        result = merge(result, instrument_sound, absolute_note.note_on_sample)
    return result


def percussion_list_to_sound(track, percussion_bank):
    result = []
    for absolute_percussion in sorted(track):
        if absolute_percussion.index in percussion_bank:
            instrument = percussion_bank[absolute_percussion.index]
            instrument_sound = instrument(absolute_percussion)
            result = merge(result, instrument_sound, absolute_percussion.note_on_sample)
    return result


def loop(track, times, offset):
    result = []
    for i in range(times):
        for absolute_event in track:
            result.append(absolute_event.copy(offset * i))
    return result


def percussion_sequence_to_sound(track, srate=None):
    """
    Turns list of (instrument, duration, velocity) tuples into sound.
    """
    srate = get_srate(srate)
    duration = 1.0
    velocity = 0.7
    t = 0.0
    result = []
    for tple in track:
        if hasattr(tple,'__getitem__'):
            instrument = tple[0]
            if len(tple) > 1:
                duration = tple[1]
                if len(tple) > 2:
                    velocity = tple[2]
        else:
            instrument = tple
        instrument_sound = instrument(Percussion(velocity=velocity, srate=srate))
        result = merge(result, instrument_sound, int(t * srate))
        t += duration
    return result


#TODO: percussion_sequence_to_sound_gen
