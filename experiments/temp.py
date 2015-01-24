from math import *
from scipy.special import dawsn

epsilon = 1e-10


# TODO: Needs work.
def dawson(x):
    y = abs(x)
    if (y < epsilon):
        return x
    elif y < 0.5:
        x2 = x * x
        return x * (1 + x2 * (-0.6666666666666666 + x2 * (0.26666666666666666 + x2 * (-0.0761904761904762 + x2 * (0.016931216931216932 + x2 * (-0.0030784030784030783 + x2 * (0.0004736004736004736 - 0.00006314672981339648 * x2)))))))
    elif y < 1:
        return copysign(0.000010261503077807835 + y * (0.9997316141131062 + y * (0.002560608208595938 + y * (-0.6798977434516322 + y * (0.04281708942217932 + y * (0.1740808317471772 + y * (0.13698283243819914 + y * (-0.21355265381336802 + (0.08813961149733342 - 0.01279294671005895 * y) * y))))))), x)
    elif y < 1.5:
        return copysign(-0.0297610182845926 + y * (1.2408802903207512 + y * (-0.8738040360463102 + y * (1.197407946828618 + y * (-2.5723248892153565 + y * (2.6335117325960793 + y * (-1.426250919499882 + y * (0.43465674463806214 + (-0.07112133631724929 + 0.004884989659896305 * y) * y))))))), x)
    elif y < 2:
        return copysign(0.3280171850502305 + y * (-0.6976885721491382 + y * (3.792306980938873 + y * (-5.346490664221177 + y * (3.315069254665668 + y * (-0.8858822943107625 + y * (-0.030749414094051297 + y * (0.0815688682796855 + (-0.019569312754026093 + 0.0015926064653226208 * y) * y))))))), x)
    elif y < 2.5:
        return copysign(1.1029282191800833 + y * (-4.494977185149537 + y * (12.032231278724579 + y * (-15.749026655727278 + y * (11.741937896447302 + y * (-5.431320411413569 + y * (1.6026458629700011 + y * (-0.2956554950575279 + (0.03125255172638591 - 0.0014515304919097605 * y) * y))))))), x)
    else:
        ix = 1 / x
        ix2 = ix * ix
        return ix * (0.5 + ix2 * (0.25 + ix2 * (0.375 + ix2 * (0.9375 + ix2 * (3.28125 + ix2 * (14.765625 + ix2 * (81.2109375 + 527.87109375 * ix2)))))))

def theta_complement(phase, sharpness):
    """Hilbert transform of the theta function. (Antisymmetric)"""
    q = sharpness
    if q < epsilon:
        return sin(two_pi * phase)
    if q < 0.5:
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9

        c = cos(two_pi * phase)
        s = sin(two_pi * phase)
        s_2 = s * s
        s2 = 2 * s * c
        s3 = s * (3 - 4 * s_2)
        s4 = 4 * s * (c * c - 0.5)
        s5 = s * (5 + s_2 * (16 * s_2 - 20))

        return (q * s + q4 * s2 + q9 * s3 + q16 * s4 + q25 * s5) / (q + q4 + q9 + q16 + q25)
    else:
        t = phase - floor(phase + 0.5)
        i_log_q = 1 / log(q)
        a = pi_squared * i_log_q

        b = exp(a)
        b4 = b ** 4

        c = 0.5 * sqrt(-pi * i_log_q)

        return 2 / sqrt(pi) * sum(dawson(sqrt(-a) * (t - n)) for n in range(-10, 11)) * c / ((1 + 2 * (b + b4)) * c - 0.5)

theta_c = theta_complement


xs = [i * 0.0001 for i in range(3000)]

print max(abs(dawson(x) - dawsn(x)) for x in xs)

def float_list_to_bytes(l):
    bs = bytearray()
    for f in l:
        mantissa, exponent = frexp(f)
        mantissa = int(mantissa * 256 ** 6)
        exponent = max(0, min(255, exponent + 128))
        bs.extend(mantissa.to_bytes(6, 'big'))
        bs.append(exponent)
    return bytes(bs)


bs = float_list_to_bytes([1,2,3,6.45,23.231])

import zlib

print (hex(int.from_bytes(zlib.compress(bs, level=9), 'big')))


def smooth_noise(frequency, order=3, leak_constant=0.99, srate=None):
    srate = get_srate(srate)
    dt = 1.0 / srate
    frequency = to_iterable(frequency)

    ns = [0] * order
    rn = range(order)
    y = [0] * (order + 1)
    r = range(order)

    target = 1.0
    phase = target
    while True:
        if phase >= target:
            ns.insert(0, random() - 0.5)
            for i in rn:
                ns[i + 1] -= ns[i]
            n = ns.pop()
            phase = phase % target
            target = random() + random()
        y[0] = n
        for i in r:
            y[i + 1] = y[i] + y[i + 1] * leak_constant
        yield y[-1]

        phase += dt * next(frequency)


"""
    void linear_sequence_to_list(double xs[], size_t len_xs, double css[], size_t len_css, double srate, double result[])
    {
        size_t i, j, samples;
        double dx, l, a, b, accumulator, da;
        size_t k = 0;
        double dt = 1.0 / srate;
        double x = xs[0];

        for (i = 0; i < len_xs - 1; i++){
            dx = x - xs[i];
            l = xs[i + 1] - x;
            if (l <= 0){
                continue;
            }
            if (i < len_xs - 2){
                samples = (size_t) ceil(l * srate);
            }
            else {
                samples = (size_t) floor(l * srate);
            }
            a = css[2 * i];
            b = css[2 * i + 1];
            accumulator = dx * a + b;
            da = a * dt;
            for (j = 0; j < samples; j++){
                result[k++] = accumulator;
                accumulator += da;
            }
            x += samples * dt;
        }
    }
"""

def linear_sequence_to_list(ls):
    xs = ffi.new("double[]", ls.xs)
    css = ffi.new("double[]", list(chain(*ls.coefficientss)))
    result = ffi.new("double[]", ls.samples())
    srate = get_srate(ls.srate)
    C.linear_sequence_to_list(xs, len(xs), css, len(css), srate, result)
    return list(result)


def snowy_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    srate = get_srate(srate)
    dt = 1 / srate
    frequency = to_iterable(frequency)

    y1 = uniform(vmin=vmin, vmax=vmax)
    y2 = uniform(vmin=vmin, vmax=vmax)
    phase = srate
    for sample in frequency:
        if phase >= srate:
            y0, y1 = y1, y2
            y2 = uniform(vmin=vmin, vmax=vmax)
            phase = phase % srate
            dp0 = (y1 - y0) * dt
            dp = (y2 - y1) * dt
        # The idea is to add analytic zeroes with delay filters to lowpass the noise
        if 3 * phase < srate:
            d3 = y0 + dp0 * (phase + 2 * srate / 3)
        else:
            d3 = y1 + dp * (phase - srate / 3)
        yield (y1 + dp * phase + d3) * 0.5
        phase += sample