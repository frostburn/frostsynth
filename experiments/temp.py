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
