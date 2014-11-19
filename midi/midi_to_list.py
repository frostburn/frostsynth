# Midi is only supported in 2.x
from pprint import pprint

import midi


class Note(object):
    def __init__(self, event, note_on_time):
        self.pitch = event.get_pitch()
        self.note_on_velocity = event.get_velocity() / 127.0
        self.note_on_time = note_on_time

    def note_off(self, event, note_off_time):
        self.duration = note_off_time - self.note_on_time
        self.note_off_velocity = event.get_velocity() / 127.0

    def __lt__(self, other):
        return self.note_on_time < other.note_on_time

    def __repr__(self):
        return "AbsoluteNote(pitch=%s, note_on_time=%s, note_on_velocity=%s, duration=%s, note_off_velocity=%s)" % (
            pitch_names[self.pitch], self.note_on_time, self.note_on_velocity, self.duration, self.note_off_velocity
        )


class Percussion(object):
    def __init__(self, event, note_on_time):
        self.index = event.get_pitch()
        self.velocity = event.get_velocity() / 127.0
        self.note_on_time = note_on_time

    def __lt__(self, other):
        return self.note_on_time < other.note_on_time

    def __repr__(self):
        return "AbsolutePercussion(index=%s, note_on_time=%s, velocity=%s)" % (self.index, self.note_on_time, self.velocity)


pitch_names = {}
for octave in range(10):
    for i, key in enumerate(["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]):
        name = key + str(octave)
        value = 12 * (octave + 1) + i
        pitch_names[value] = name

percussion_map = {36: "Bass Drum", 42: "Closed Hi-Hat", 28: "Snare Drum"}

pattern = midi.read_midifile("organ_groove.midi")
#pattern.make_ticks_rel()
tempo = 500000
resolution = float(pattern.resolution)
tick_time = tempo / resolution / 1000000.0
#track = pattern[0]

for track in pattern:
    notes = [0.0] * 128
    result = []
    running_tick = 0
    for event in track:
        running_tick += event.tick
        time = running_tick * tick_time
        is_percussion = isinstance(event, midi.NoteEvent) and event.channel == 9
        is_note_on = isinstance(event, midi.NoteOnEvent) and event.get_velocity() > 0
        is_note_off = isinstance(event, midi.NoteOffEvent) or (isinstance(event, midi.NoteOnEvent) and event.get_velocity() == 0)
        if is_percussion:
            if is_note_on:
                result.append(Percussion(event, time))
        else:
            if is_note_on:
                notes[event.get_pitch()] = Note(event, time)
            elif is_note_off:
                note = notes[event.get_pitch()]
                note.note_off(event, time)
                result.append(note)

    pprint(sorted(result))

#print pattern
