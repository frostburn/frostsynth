import subprocess
from itertools import islice

from frostsynth import get_srate, timeslice, interlace
from frostsynth.dump import iter_dumps


def play_chunked(source, chunk_size=4096):
    source = iter(source)
    srate = int(get_srate())
    p = subprocess.Popen(["aplay", "--channels=1", "--format=S16_LE", "--rate=%d" % srate], stdin=subprocess.PIPE)
    try:
        while True:
            s = iter_dumps(islice(source, chunk_size))
            if s:
                p.stdin.write(s)
            else:
                break
    finally:
        p.communicate()

def play(source, duration=None):
    source = iter(source)
    srate = int(get_srate())
    p = subprocess.Popen(["aplay", "--channels=1", "--format=S16_LE", "--rate=%d" % srate], stdin=subprocess.PIPE)
    try:
        if duration is None:
            p.stdin.write(iter_dumps(source, 2))
        else:
            p.stdin.write(timeslice(iter_dumps(source, 2), duration))
    finally:
        p.communicate()


def stereo_play(left, right):
    source = interlace(left, right)
    srate = int(get_srate())
    p = subprocess.Popen(["aplay", "--channels=2", "--format=S16_LE", "--rate=%d" % srate], stdin=subprocess.PIPE)
    try:
        p.stdin.write(iter_dumps(source, 2))
    finally:
        p.communicate()