from cmath import exp, pi


_twiddle_factors = {}


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    if N & (N - 1) != 0:
        raise ValueError("Only power of two lengths supported.")
    even = fft(x[0::2])
    odd =  fft(x[1::2])
    if N in _twiddle_factors:
        twiddle = _twiddle_factors[N]
    else:
        twiddle = [exp(-2j * pi * k / N) for k in range(N // 2)]
        _twiddle_factors[N] = twiddle
    return [even[k] + twiddle[k] * odd[k] for k in range(N // 2)] + \
           [even[k] - twiddle[k] * odd[k] for k in range(N // 2)]


def ifft(x):
    N = len(x)
    return [z.conjugate() / N for z in fft([z.conjugate() for z in x])]


def rfft(x):
    N = len(x)
    if N <= 1:
        return x
    if N & (N - 1) != 0:
        raise ValueError("Only power of two lengths supported.")
    even = fft(x[0::2])
    odd =  fft(x[1::2])
    if N in _twiddle_factors:
        twiddle = _twiddle_factors[N]
    else:
        twiddle = [exp(-2j * pi * k / N) for k in range(N // 2)]
        _twiddle_factors[N] = twiddle
    return [even[k] + twiddle[k] * odd[k] for k in range(N // 2)] + [even[0] - odd[0]]


def irfft(x):
    return [z.real for z in ifft(x + [0.0] * (len(x) - 2))]


def pad(x):
    N = 1
    while N < len(x):
        N <<= 1
    return x + [0.0] * (N - len(x))
