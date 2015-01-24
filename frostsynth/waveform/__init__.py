from math import *
from cmath import rect as from_polar, exp as cexp

from frostsynth import epsilon, clip, two_pi, i_pi, pi_squared
from frostsynth.ffi import precycloid


from frostsynth.waveform.saw import *
from frostsynth.waveform.theta import *


def twine(phase):
    x = phase - floor(phase + 0.5)
    #return sin(2 * asin(x + x))
    return 4 * x * sqrt(1 - 4 * x * x)


def sqrtwf(phase):
    x = phase - floor(phase + 0.5)
    if x > 0.0:
        return sqrt(32 * x) - 8 *x
    else:
        return -sqrt(-32 * x) - 8 * x


def halfcircle(phase):
    x = phase - floor(phase + 0.5)
    return sqrt(1 - 4 * x * x)


def halfcircleb(phase):
    x = phase - floor(phase + 0.5)
    return sqrt(1.6211389382774044 - 6.484555753109618 * x * x) - 1


def pinch(phase):
    phase += 0.75
    x = phase - floor(phase + 0.5)
    return atan(atanh(0.99 - 1.98 * abs(x + x))) * 0.82675935153194158


def tang(phase):
    x = phase - floor(phase + 0.5)
    return (tanh(tan(pi * phase)) - x - x) * 3.5686502577037404


def tooth(phase):
    return tanh(tan(pi * phase) ** 2) * 2 -1


def toothb(phase):
    return tanh(tan(pi * phase) ** 2) * 1.643545436007719 -1


half_pi = 0.5 * pi


def tri(phase):
    x = phase - floor(phase + 0.5)
    return tanh(tan(two_pi * abs(x) - half_pi))


one_per_pi = 1 / pi
two_per_pi = 2 / pi
four_thirds_per_pi = 4 / (3 * pi)
four_fifths_per_pi = 4 / (5 * pi)
four_sevenths_per_pi = 4 / (7 * pi)
four_ninths_per_pi = 4 / (9 * pi)
four_elevenths_per_pi = 4 / (11 * pi)
pi_per_twelve = pi / 12
pi_per_ten = pi / 10
pi_per_eight = pi / 8
pi_per_six = pi / 6
half_pi = 0.5 * pi
three_pi = 3 * pi
four_pi = 4 * pi
five_pi = 5 * pi
six_pi = 6 * pi
eight_pi = 8 * pi
ten_pi = 10 * pi
twelve_pi = 12 * pi


def lissajous11(phase, sharpness=0):
    if abs(sharpness) < epsilon:
        return sin(two_pi * phase)
    x = pi * (phase - floor(phase + 0.5))
    s = clip(sharpness, epsilon - 1, 1 - epsilon)
    a = 1 + s
    b = 1 - s
    return (atan2(a * a * sin(x), b * b * cos(x)) - x) / (2 * atan2(b, a) - half_pi)


def lissajous12(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = half_pi * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(two_pi * phase), (1 - s) * cos(four_pi * phase + b)) * four_thirds_per_pi


def lissajous13(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(three_pi * x), (1 - s) * cos(pi * x + b)) * two_per_pi + x + x


def lissajous14(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = pi_per_eight * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 - s) * cos(two_pi * phase + b), (1 + s) * cos(eight_pi * phase)) * 0.39328116619206743


def lissajous15(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(pi * x + b)) * 0.4754858297894094 - 1.4937827897524554 * x


def lissajous16(phase, sharpness=0, bias=0):
    s = clip(sharpness, -1, 1)
    b = half_pi * clip(bias, epsilon - 1, 1 - epsilon)
    return atan2((1 - s) * sin(two_pi * phase), (1 + s) * cos(twelve_pi * phase + b)) * 0.3708887239244341


def lissajous23(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(six_pi * x), (1 - s) * cos(four_pi * x + b))
    if x > 0 and l < 0:
        l += two_pi
    elif x < 0 and l > 0:
        l -= two_pi
    return l * four_fifths_per_pi


def lissajous25(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((-1 - s) * sin(ten_pi * x), (1 - s) * cos(four_pi * x + b))
    if 0.15 < x < 0.35 and l < 0:
        l += two_pi
    elif -0.35 < x < -0.15 and l > 0:
        l -= two_pi
    return l * four_fifths_per_pi


def lissajous34(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_six * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 - s) * sin(six_pi * x), (1 + s) * cos(eight_pi * x + b))
    if 0.1 < x < 0.4 and l < 0:
        l += two_pi
    elif -0.4 < x < -0.1 and l > 0:
        l -= two_pi
    return l * four_sevenths_per_pi


def lissajous35(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(five_pi * x), (1 - s) * cos(three_pi * x + b))
    if x > 0 and l < 0:
        l += two_pi
    elif x < 0 and l > 0:
        l -= two_pi
    return l * one_per_pi - x


def lissajous45(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 + s) * sin(ten_pi * x), (1 - s) * cos(eight_pi * x + b))
    if (x > 0 and l < 0) or (0.15 < x < 0.35):
        l += two_pi
    elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
        l -= two_pi
    return l * four_ninths_per_pi


def lissajous56(phase, sharpness=0, bias=0):
    x = phase - floor(phase + 0.5)
    s = clip(sharpness, -1, 1)
    b = pi_per_ten * clip(bias, epsilon - 1, 1 - epsilon)
    l = atan2((1 - s) * sin(ten_pi * x), (1 + s) * cos(twelve_pi * x + b))
    if (x > 0 and l < 0) or (0.15 < x < 0.35):
        l += two_pi
    elif (x < 0 and l > 0) or (-0.35 < x < -0.15):
        l -= two_pi
    return l * four_elevenths_per_pi


def rect(phase, duty=0.5):
    x = phase - floor(phase)
    if x < duty:
        return 1.0
    else:
        return 0.0


def square(phase, bias=0.5):
    x = phase - floor(phase)
    if x < bias:
        return 1.0
    else:
        return -1.0


def circle(phase, bias=0.5):
    x = phase - floor(phase)
    bias = clip(bias, epsilon, 1.0 - epsilon)
    if x < bias:
        return sqrt(x * (bias - x) * 4 / (bias * bias))
    else:
        return -sqrt((x - bias) * (1 - x) * 4 / (1 + bias * (bias - 2)))


def circleb(phase, bias=0.5):
    return circle(phase, bias) - 1.5707963267948966 * bias + 0.7853981633974483


def triangle(phase, bias=0.5):
    x = phase - floor(phase)
    bias = clip(bias, epsilon, 1.0 - epsilon)
    if x < bias:
        return (x + x) / bias - 1.0;
    else:
        x -= bias;
        return 1.0 - (x + x) / (1.0 - bias)


def triangle0(phase, bias=0.5):
    return triangle(phase + 0.5 * bias, bias)


def parangle(phase, bias=0.5):
    x = phase - floor(phase)
    bias = clip(bias, epsilon, 1.0 - epsilon)
    if x < bias:
        return 8 * x * (bias - x) / bias;
    else:
        return 8 * (x - bias) * (x - 1) / (1 - bias)


def parangleb(phase, bias=0.5):
    return parangle(phase, bias) + 1.3333333333333333 - 2.6666666666666666 * bias


def paranglen(phase, bias=0.5):
    return parangle(phase, bias) + 1 - 2 * bias


def cubangle(phase, bias=0.5):
    x = triangle(phase, bias)
    return x * (1.5 - 0.5 * x * x)


def tent(phase, bias=0.5):
    x = triangle(phase, bias)
    return x ** 3


def quarangle(phase, bias=0.5):
    x = phase - floor(phase)
    bias = clip(bias, epsilon, 1.0 - epsilon)
    if x < bias:
        return 2 * bias * (1 - (2 * x / bias - 1) ** 4)
    else:
        return 2 * (1 - bias) * ((2 * (x - bias) / (1 - bias) - 1) ** 4 - 1)


def quarangleb(phase, bias=0.5):
    return quadangle(phase, bias) + 1.6 - 3.2 * bias


def quaranglen(phase, bias=0.5):
    return quadangle(phase, bias) + 1 - 2 * bias


def tense(phase, bias=0.5, tension=2):
    x = phase - floor(phase)
    bias = clip(bias, epsilon, 1.0)
    if tension < 0.0:
        tension = 0.0
    if x < bias:
        return 1.0 - 2.0 * (x / bias) ** tension
    else:
        return 0


def softsaw(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - epsilon)
    return atan(s * sin(x) / (1.0 + s * cos(x))) / asin(s)


def softsaw_complement(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - 100 * epsilon)
    return 0.5 * log(1 + (s - 2 * cos(x)) * s) / asin(s)


def _softsquare(phase, sharpness, bias=0.5):
    return softsaw(phase + 0.5 - bias, sharpness) - softsaw(phase + 0.5, sharpness)


def softrect(phase, sharpness, bias=0.5):
    bottom = _softsquare(0.5 + bias * 0.5, sharpness, bias)
    top = softsquare2(0.5 * bias, sharpness, bias)
    return (softsquare2(phase, sharpness, bias) - bottom) / (top - bottom)


def softrect2(phase, tension, duty=0.5):
    if tension < epsilon:
        tension = epsilon
    c = cos(pi * duty)
    top = tanh(tension * (1 + c))
    bottom = tanh(tension * (c - 1))
    return (top - tanh(tension * (cosine(phase) + c))) / (top - bottom)


def softsquare(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - epsilon)
    a = 2 * s / (1 - s * s)
    return atan(a * sin(x)) / atan(a)


def softsquare2(phase, tension, bias=0.5):
    if tension < epsilon:
        tension = epsilon
    c = cos(pi * bias)
    top = tanh(tension * (1 + c))
    bottom = tanh(tension * (c - 1))
    return 2 * (tanh(tension * (cosine(phase) + c)) - bottom) / (top - bottom) - 1


def softsquare3(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon - 1, 1 - epsilon)
    return sin(x) / sqrt(1 - s * cos(x) ** 2)


def pcycloid(phase, sharpness=1):
    if abs(sharpness) < epsilon:
        return sin(two_pi * phase)
    else:
        x = (phase - floor(phase)) * two_pi
        s = clip(sharpness, -1, 1)
        return (x - precycloid(x, s)) / s


def cycloid(phase, sharpness=1):
    return cos(precycloid(two_pi * phase, clip(sharpness, -1, 1)))


def softarc(phase, sharpness):
    if sharpness < epsilon:
        return cos(two_pi * phase)
    elif sharpness < 1:
        return (hypot((1 + sharpness) * cos(pi * phase), (1 - sharpness) * sin(pi * phase)) - 1) / sharpness
    else:
        return abs(cos(pi * phase)) * 2 - 1


def softtriangle(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - epsilon)
    return asin(s * sin(x)) / asin(s)


two_pi_squared = 2 * pi_squared
half_pi_squared = 0.5 * pi_squared


def sineh(phase, sharpness):
    if sharpness < epsilon:
        return sin(two_pi * phase)
    elif sharpness < 0.99:
        a = sharpness / (1 - sharpness)
        return sinh(a * sin(two_pi * phase)) / sinh(a)
    elif sharpness < 1:
        x = phase - floor(phase)
        a = -two_pi_squared * sharpness / (1 - sharpness)
        return exp(a * (x - 0.25) * (x - 0.25)) - exp(a * (x - 0.75) * (x - 0.75))
    else:
        return 0.0


def cosineh(phase, sharpness):
    if sharpness < epsilon:
        return 0.5 + 0.5 * cos(two_pi * phase)
    elif sharpness < 0.99:
        a = sharpness / (1 - sharpness)
        return (cosh(a * cos(pi * phase)) - 1) / (cosh(a) - 1)
    elif sharpness < 1:
        x = phase - floor(phase + 0.5)
        a = -half_pi_squared * sharpness / (1 - sharpness)
        return exp(a * x * x)
    else:
        return 0.0


def formant(phase, ratio, width):
    """Formant waveform with energy concentrated on the harmonic specified by ratio."""
    ratio = floor(ratio)
    if width < 700:
        x = pi * phase
        return cosh(cos(x) * width) / cosh(width) * cos(2 * x * ratio)
    else:
        x = phase - floor(phase + 0.5)
        return exp(-half_pi_squared * width * x * x) * cos(two_pi * x * ratio)


def tentfold(phase, level, bias=0.5, iterations=5):
    bias = clip(bias, epsilon, 1 - epsilon)
    bias1 = 1 - bias
    level = clip(bias + level * bias1, bias, 1)
    x = phase - floor(phase)
    m0 = level / bias
    m1 = level / bias1
    for _ in range(iterations):
        if x < bias:
            x *= m0
        else:
            x = (1 - x) * m1
    return 2 * x / level - 1


def parfold(phase, level, iterations=5, scale=0.99):
    r = clip(2 + 2 * level, 2, 4)
    x = phase - floor(phase)
    x = 0.5 * (1 - scale) + x * scale
    for _ in range(iterations):
        x = r * x * (1 - x)
    return 8 * x / r - 1


def cosfold(phase, level, iterations=5):
    x = phase - floor(phase)
    level = clip(0.5 * level, epsilon, 0.5)
    for _ in range(iterations):
        x = (1 - cos(two_pi * x)) * level
    return x / level - 1


def sinfold(phase, level, bias=0, iterations=5):
    phase = sin(phase * two_pi)
    for _ in range(iterations):
        phase = sin((phase * level + bias) * two_pi)
    return phase


def sine(phase):
    return sin(two_pi * phase)


def cosine(phase):
    return cos(two_pi * phase)


def rsine(phase, vmin=0.0, vmax=1.0):
   return vmin  + (sin(two_pi * phase) + 1) * 0.5 * (vmax - vmin)


def rcosine(phase, vmin=0.0, vmax=1.0):
   return vmin  + (1 - cos(two_pi * phase)) * 0.5 * (vmax - vmin)


def cis(phase):
    return from_polar(1, two_pi * phase)


def duplex(func, phase, bias=0.5):
    return func(phase - bias * 0.5) - func(phase + bias * 0.5)


def duplexn(func, phase, bias=0.5):
    bias = clip(bias, epsilon, 1 - epsilon)
    return (func(phase - bias * 0.5) - func(phase + bias * 0.5)) / (0.5 - abs(0.5 - bias)) * 0.25


def raised(func, phase, vmin=0.0, vmax=1.0):
    return vmin + (func(phase) + 1) * 0.5 * (vmax - vmin)


def raised0(func, phase, vmin=0.0, vmax=1.0):
    return vmin + func(phase) * (vmax - vmin)


def bias(phase, bias=0.5):
    x = phase - floor(phase)
    if x < bias:
        return 0.5 * x / bias
    else:
        return 0.5 + 0.5 * (x - bias) / (1 - bias)
