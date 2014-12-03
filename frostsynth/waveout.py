import wave

from frostsynth import get_srate, timeslice, interlace
from frostsynth.dump import iter_dumps


def save(source, filename, duration=None):
    f = wave.open(filename,"wb")
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(int(get_srate()))
    try:
        if duration is None:
            f.writeframes(iter_dumps(source, f.getsampwidth()))
        else:
           f.writeframes(iter_dumps(timeslice(source, duration), f.getsampwidth()))
    finally:
        f.close()


def stereo_save(left, right, filename):
    source = interlace(left, right)
    f = wave.open(filename,"wb")
    f.setnchannels(2)
    f.setsampwidth(2)
    f.setframerate(int(get_srate()))
    try:
        f.writeframes(iter_dumps(source, f.getsampwidth()))
    finally:
        f.close()
