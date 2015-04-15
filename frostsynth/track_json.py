from collections import defaultdict
import json
import logging

from frostsynth.track import TrackContext, AbsoluteNote
from frostsynth.polysequence import LinearSequence


logger = logging.getLogger(__name__)


def add_control_points(data, delta=0.02):
    new_data = []
    prev_x = -float('inf')
    prev_y = 0.0
    for datum in data:
        x, y = datum
        if x - prev_x > delta:
            new_data.append((x - delta, prev_y))
        new_data.append(datum)
        prev_x = x
        prev_y = y
    return new_data


def _process(data, controller_map=None):
    logger.info('Processing JSON track data.')
    if controller_map is None:
        controller_map = {}
    srate = data.get('sampling rate', 44100)
    initial_time_tag = data.get('initial time tag', 0)
    tag_rate = 1000
    events = data.get('events', [])
    events.sort(key=lambda e: e['sample'])
    last_time_tag = 0
    time_tag_delta = 0
    for event in events:
        time_tag = event['time tag'] - initial_time_tag
        if time_tag < last_time_tag:
            time_tag_delta += 2 ** 16
        last_time_tag = time_tag
        time_tag += time_tag_delta
        t = event['sample'] / srate
        fuzzy_t = time_tag / tag_rate
        while fuzzy_t < t - 10:
            time_tag += 2 ** 16
            time_tag_delta += 2 ** 16
            fuzzy_t = time_tag / tag_rate
        event['time tag'] = time_tag
    event = events[-1]
    if (event['sample'] != 0):
        tag_rate = srate * event['time tag'] / event['sample']
    logger.info('Tag rate: %g', tag_rate)

    max_delta_t = 0.0
    controllers = defaultdict(list)
    for event in events:
        t = event['time tag'] / tag_rate
        max_delta_t = max(max_delta_t, abs(t - event['sample'] / srate))
        if event['type'] not in ['note on', 'note off']:
            name = controller_map.get(event['type'], event['type'])
            controllers[name].append((t, event['value']))
    for key, value in controllers.items():
        controllers[key] = add_control_points(value)
    for key, value in controllers.items():
        controllers[key] = LinearSequence(value, clamped=True)
    context = TrackContext(controllers)

    note_ons = {}
    notes = []
    for event in events:
        t = event['time tag'] / tag_rate
        if event['type'] == 'note on':
            if event['key'] in note_ons:
                raise ValueError('Inconsistent note on event')
            note_ons[event['key']] = (t, event['frequency'], event['velocity'])
        elif event['type'] == 'note off':
            if event['key'] not in note_ons:
                raise ValueError('Inconsistent note off event')
            note_on_time, frequency, note_on_velocity = note_ons.pop(event['key'])
            duration = t - note_on_time
            note_off_velocity = event['velocity']
            notes.append(AbsoluteNote(
                frequency=frequency,
                note_on_time=note_on_time,
                note_on_velocity=note_on_velocity,
                duration=duration,
                note_off_velocity=note_off_velocity,
                context=context
            ))

    logger.info('Maximum time slack: %g ms', max_delta_t * 1000)
    return notes, context


def load(filename, controller_map=None):
    if hasattr(filename, 'read'):
        return _process(json.load(filename), controller_map=controller_map)
    else:
        with open(filename, 'r') as f:
            return _process(json.load(f), controller_map=controller_map)
