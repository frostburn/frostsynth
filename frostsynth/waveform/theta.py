from math import *
from cmath import rect as from_polar, exp as cexp

from frostsynth import epsilon, clip, two_pi, i_pi, pi_squared
from frostsynth.numeric import cubic_approximate
from frostsynth.additive import sin_sum


#TODO: Clenshaw


def theta(phase, sharpness):
    """DC-blocked peak-amplitude normalized EllipticTheta(3, pi * phase, sharpness)"""
    q = sharpness
    if q < epsilon:
        return cos(two_pi * phase)
    if q < 0.2:
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9

        c = cos(two_pi * phase)
        c2 = 2 * c * c - 1
        c3 = 2 * c * c2 - c
        c4 = 2 * c * c3 - c2
        c5 = 2 * c * c4 - c3

        return (q * c + q4 * c2 + q9 * c3 + q16 * c4 + q25 * c5) / (q + q4 + q9 + q16 + q25)
    elif q < 0.9:
        t = phase - floor(phase + 0.5)
        i_log_q = 1 / log(q)
        a = pi_squared * i_log_q
        m = exp(-a * 2 * t)
        b = exp(a)
        b4 = b ** 4

        z2 = m * m
        z3 = m * z2
        z4 = m * z3
        s = z2 + b * (m + z3) + b4 * (1 + z4)

        c = 0.5 * sqrt(-pi * i_log_q)

        return (exp(a * t * (t + 4)) * s * c - 0.5) / ((1 + 2 * (b + b4)) * c - 0.5)
    elif q < 1:
        t = phase - floor(phase + 0.5)
        i_log_q = 1 / log(q)
        a = pi_squared * i_log_q
        c = 0.5 * sqrt(-pi * i_log_q)
        return (exp(a * t * t) * c - 0.5) / (c - 0.5)
    else:
        return 0


def theta_rect(phase, sharpness):
    """Peak-amplitude normalized EllipticTheta(3, pi * phase, sharpness)"""
    q = sharpness
    if q < epsilon:
        q = epsilon
    if q < 0.2:
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9

        c = cos(two_pi * phase)
        c2 = 2 * c * c - 1
        c3 = 2 * c * c2 - c
        c4 = 2 * c * c3 - c2
        c5 = 2 * c * c4 - c3

        return (1 + 2 * (q * c + q4 * c2 + q9 * c3 + q16 * c4 + q25 * c5)) / (1 + 2 * (q + q4 + q9 + q16 + q25))
    elif q < 0.9:
        t = phase - floor(phase + 0.5)
        a = pi_squared / log(q)
        m = exp(-a * 2 * t)
        b = exp(a)
        b4 = b ** 4

        z2 = m * m
        z3 = m * z2
        z4 = m * z3
        s = z2 + b * (m + z3) + b4 * (1 + z4)

        return exp(a * t * (t + 4)) * s / (1 + 2 * (b + b4))
    elif q < 1:
        t = phase - floor(phase + 0.5)
        a = pi_squared / log(q)
        return exp(a * t * t)
    else:
        return 0


def theta_integral(phase, sharpness):
    """Peak-amplitude normalized integral of DC-blocked EllipticTheta(3, pi * phase, sharpness)"""
    q = sharpness
    if q < epsilon:
        return sin(two_pi * phase)
    elif q < 0.2:
        coefs = [q ** (n * n) / n for n in range(1, 6)]
        return sum(c * sin(two_pi * n * phase) for n, c in enumerate(coefs, 1)) / sum(coefs)
    elif q < 1:
        x = phase - floor(phase + 0.5)
        a = pi * (-log(q)) ** -0.5
        return (sum(erf(a * (x - n)) for n in range(-2 , 3)) - x - x) / ((1 - sqrt(1 - q)) * (1.2575842100262158 - 0.2575842100262158 * q))
    else:
        return -saw(phase + 0.5)


def theta_formant(phase, ratio, width):
    """Formant waveform with energy concentrated on the fractional harmonic specified by ratio."""
    if width < epsilon:
        width = epsilon
    if width < 7:
        x = two_pi * phase
        q = exp(-pi_squared / width)
        q2 = q * q
        q4 = q2 * q2
        q8 = q4 * q4
        q9 = q8 * q
        q16 = q8 * q8
        q25 = q16 * q9
        norm = 1 + 2 * (q + q4 + q9 + q25)
        floor_ratio = floor(ratio)
        ratio -= floor_ratio
        cn = cos(x * (floor_ratio - 5))
        cn1 = cos(x * (floor_ratio - 4))
        c = cos(x)
        s = cn1 * q ** (4 + ratio) ** 2
        for n in range(-3, 5):
            cn1, cn = 2 * c * cn1 - cn, cn1
            s += cn1 * q ** (n - ratio) ** 2
        return s / norm
    elif width < 100:
        x = phase - floor(phase + 0.5)
        ratio *= two_pi
        z = from_polar(1, ratio * (x + 2))
        m = cexp(2 * width * x - 1j * ratio)
        b = exp(-width)
        b4 = b ** 4

        z0 = z.real
        z *= m
        z1 = z.real
        z *= m
        s = z.real
        z *= m
        s += (z.real + z1) * b
        z *= m
        s += (z.real + z0) * b4

        return exp(-width * x * (x + 4)) * s / (1 + 2 * (b + b4))
    else:
        x = phase - floor(phase + 0.5)
        return exp(-width * x * x) * cos(two_pi * x * ratio)



def _elliptic_theta3_q(q):
    if abs(q) >= 1:
        return ValueError
    else:
        s = 1
        n = 1
        while True:
            old_s = s
            s += 2 * q ** n ** 2
            if s == old_s:
                return s
            n += 1


def _elliptic_theta3_dq(q):
    if abs(q) >= 1:
        return ValueError
    else:
        s = 0
        n = 1
        while True:
            old_s = s
            n2 = n * n
            s += 2 * n2 * q ** (n2 - 1)
            if s == old_s:
                return s
            n += 1


_et3 = cubic_approximate(_elliptic_theta3_q, _elliptic_theta3_dq, 0, 0.99, 1000)


def theta_formant_complement(phase, ratio, width, accuracy_goal=1e-5):
    q = exp(-pi_squared / width)
    if q > 0.99:
        raise ValueError
    ratio = abs(ratio)
    n = 1
    coefs = []
    while True:
        coef = q ** (n - ratio) ** 2
        if coef < accuracy_goal and n > ratio:
            break
        coefs.append(coef)
        n += 1
    n = 1
    while True:
        coef = q ** (n + ratio) ** 2
        if coef < accuracy_goal:
            break
        coefs[n - 1] += coef
        n += 1
    return sin_sum(phase, coefs) / _et3(q)


theta_formant_c = theta_formant_complement
