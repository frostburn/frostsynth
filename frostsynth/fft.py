from cmath import exp as cexp, pi

_twiddle_factors = {}

try:
    from ffi import fft
except:
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
            twiddle = [cexp(-2j * pi * k / N) for k in range(N // 2)]
            _twiddle_factors[N] = twiddle
        return [even[k] + twiddle[k] * odd[k] for k in range(N // 2)] + \
               [even[k] - twiddle[k] * odd[k] for k in range(N // 2)]


def ifft(x):
    i_N = 1.0 / len(x)
    return [z.conjugate() * i_N for z in fft([z.conjugate() for z in x])]


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
        twiddle = [cexp(-2j * pi * k / N) for k in range(N // 2)]
        _twiddle_factors[N] = twiddle
    return [even[k] + twiddle[k] * odd[k] for k in range(N // 2)] + [even[0] - odd[0]]


def _irfft_process(x):
    return [x[0]] + [2 * b for b in x[1:-1]] + [x[-1]] + [0.0j] * (len(x) - 2)


def irfft(x):
    return [z.real for z in ifft(_irfft_process(x))]


def unnormalized_ifft(x):
    return [z.conjugate() for z in fft([z.conjugate() for z in x])]


def unnormalized_irfft(x):
    return [z.real for z in unnormalized_ifft(_irfft_process(x))]


def pseudo_irfft(x):
    return [z.real for z in fft(_irfft_process(x))]


def pseudo_norm_irfft(x):
    m = ((len(x) - 1) * 2) ** -0.5
    return [m * z.real for z in fft(_irfft_process(x))]


def analytic_pfft(x):
    return [z for z in fft(_irfft_process(x))]


def pad(x):
    N = 1
    while N < len(x):
        N <<= 1
    return x + [0.0] * (N - len(x))

def rpad(x):
    N = 2
    while N // 2 + 1 < len(x):
        N <<= 1
    return x + [0.0] * (N // 2 + 1 - len(x))
