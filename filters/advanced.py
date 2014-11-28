from collections import deque, Sequence

from base import *
from filters.base import *
from filters.basic import *
from filters.delay import *
from ffi import convolve as convolve_list


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
    k = int(dt * srate)
    buf = []
    result = []
    for i, kernel in enumerate(kernels):
        result += buf[:k]
        buf = buf[k:]
        s = signal[i * k: (i + 1) * k]
        if not s:
            break
        c = convolve_list(s, kernel)
        if len(buf) < len(c):
            buf += [0.0] * (len(c) - len(buf))
        else:
            c += [0.0] * (len(buf) - len(c))
        buf = [b + c for b, c, in zip(buf, c)]
    result += buf
    return result


def reverb(source):
    g = 0.45
    d = 0.6
    lpf_ = lambda s: onepole(s, 1, -d, g * (1 - d))

    def lbcf(source, duration):
        return filtered_comb_t(source, duration, lpf_)

    s0, s1, s2 = tee(source, 3)
    return gain_gen(schroeder_t(schroeder_t(mix_gen([lbcf(s0, 0.035), lbcf(s1, 0.051), lbcf(s2, 0.067)]), 0.0077, 0.5), 0.0091, 0.5), 0.3)
