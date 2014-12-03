from collections import deque, Sequence

from frostsynth import *
from frostsynth.filters.base import *
from frostsynth.filters.basic import *
from frostsynth.filters.delay import *
from frostsynth.ffi import convolve as convolve_list
from frostsynth.track import A2, A4, mtof


def convolve_gen(iterable, kernel, tail=True):
    """Returns iterable convolved with kernel.

    If 'tail' is true output continues for len(kernel)-1 steps after iterable is exhausted.

    convolve([1,0,5],[1,2,3,4]) -> 1, 2, 8
    convolve([1,0,5],[1,2,3,4], True) -> 1, 2, 8, 14, 15, 20
    """   
    signal = deque(maxlen=len(kernel))

    for element in iterable:
        signal.appendleft(element)
        yield sum(s * k for s, k in zip(signal, kernel))
    if tail:
        kernel = deque(kernel)
        kernel.popleft()
        while kernel:
            yield sum(s * k for s, k in zip(signal, kernel))
            kernel.popleft()


def convolve(signal, kernel):
    if isinstance(signal, Sequence) and isinstance(kernel, Sequence):
        return convolve_list(signal, kernel)
    else:
        return convolve_gen(signal, kernel)


def dynamic_convolve(signal, kernels, dt=0.05, srate=None):
    srate = get_srate(srate)
    buf = []
    result = []
    t = 0.0
    for kernel in kernels:
        i = int(t * srate)
        t += dt
        l = int(t * srate) - i
        s = signal[i: l + i]
        if not s:
            break
        c = convolve_list(s, kernel)
        if len(buf) < len(c):
            buf += [0.0] * (len(c) - len(buf))
        else:
            c += [0.0] * (len(buf) - len(c))
        buf = [b + c for b, c, in zip(buf, c)]
        result += buf[:l]
        buf = buf[l:]
    result += buf
    return result


def lbcf(source, duration, factor, gain, srate=None):
    dur = 1.0 / 44100.0
    lpf_ = lambda s: decay(s, factor, gain, duration=dur, srate=srate)

    return filtered_comb_t(source, duration, lpf_)


def reverb(source):
    g = 0.45
    d = 0.6
    s0, s1, s2 = tee(source, 3)
    return gain_gen(schroeder_t(schroeder_t(mix_gen([lbcf(s0, 0.035, d, g), lbcf(s1, 0.051, d, g), lbcf(s2, 0.067, d, g)]), 0.0077, 0.5), 0.0091, 0.5), 0.3)


def grand_reverb(source, factor=0.3, gain=0.975, first_pitch=A2, last_pitch=A4, srate=None):
    sources = tee(source, last_pitch - first_pitch + 1)
    ls = []
    for i, s in enumerate(sources):
        ls.append(lbcf(s, 1 / mtof(first_pitch + i), factor, gain, srate=srate))
    return mix_gen(ls)
