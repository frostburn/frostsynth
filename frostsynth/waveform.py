from math import *
from cmath import rect as from_polar, exp as cexp

from frostsynth import epsilon, clip, two_pi, two_pi_j, i_pi
from frostsynth.ffi import precycloid

if False:
    __all__ = [
        "saw", "saw_complement", "par", "par_complement", "cub", "cub_complement", "qua", "pen",
        "rect", "square", "triangle", "tense",
        "softsaw", "softsaw_complement", "softrect", "softrect2", "softsquare", "softsquare2", "softsquare3", "softtriangle",
        "sine", "cosine", "cis",
        "duplex", "bias"
    ]


def saw(phase):
    x = phase - floor(phase + 0.5)
    return x + x


def saw_complement(phase):
    a = 1 + cos(two_pi * phase)
    if (a < epsilon):
        a = epsilon
    #return log(1 + cos(t)) / pi + log(2) / pi
    return log(a) * i_pi + 0.2206356001526516


sawc = saw_complement


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


def tang(phase):
    x = phase - floor(phase + 0.5)
    return (tanh(tan(pi * phase)) - x - x) * 3.5686502577037404


def par(phase):
    x = phase - floor(phase + 0.5)
    return 6 * x * x - 0.5


def par_complement(phase):
    x = phase - floor(phase + 0.5)
    if x < -0.45:
        xx = (0.5 + x)
        return xx * (-6.50377029198 + 39.1640305629 * xx) - 0.82780791828 * sqrt(xx)
    elif x < -0.4:
        return -6.52202646969 + x * (-47.7235413275 + x * (-131.454491059 - 123.496136031 * x))
    elif x < -0.35:
        return -1.22922321362 + x * (-8.5259921333 + x * (-34.7068061396 - 43.9115553199 * x))
    elif x < -0.25:
        return -0.167319598632 + x * (0.61647503263 + x * (-8.46993943614 - 18.8140327989 * x))
    elif x < -0.15:
        return -0.0107270508022 + x * (2.43730170152 + x * (-1.4197683794 - 9.72465221494 * x))
    elif x < 0.15:
        return x * (2.64762720183 - 6.4289442721 * x * x)
    elif x < 0.25:
        return 0.0107270508022 + x * (2.43730170152 + x * (1.4197683794 - 9.72465221494 * x))
    elif x < 0.35:
        return 0.167319598632 + x * (0.61647503263 + x * (8.46993943614 - 18.8140327989 * x))
    elif x < 0.4:
        return 1.22922321362 + x * (-8.5259921333 + x * (34.7068061396 - 43.9115553199 * x))
    elif x < 0.45:
        return 6.52202646969 + x * (-47.7235413275 + x * (131.454491059 - 123.496136031 * x))
    else:
        xx = (0.5 - x)
        return xx * (6.50377029198 - 39.1640305629 * xx) + 0.82780791828 * sqrt(xx)


parc = par_complement


def cub(phase):
    x = phase - floor(phase + 0.5)
    return x * (5.19615242270663188 - 20.7846096908265275 * x * x)


def cub_complement(phase):
    x = phase - floor(phase + 0.5)
    if x < -0.485:
        return -141.683313066 + x * (-890.871247193 + x * (-1877.70991482 - 1315.78489017 * x))
    elif x < -0.45:
        return -14.4841833281 + x * (-107.462486507 + x * (-269.423768994 - 215.237469947 * x))
    elif x < -0.4:
        return -2.72415704125 + x * (-29.4601745573 + x * (-96.9694386506  - 88.148440549 * x))
    elif x < -0.35:
        return -0.242340474369 + x * (-11.0004026851 + x * (-51.2046399185 + -50.3316340626 *x))
    elif x < -0.25:
        return 0.645147736088 + x * (-3.29984031237 + x * (-28.9358315141 - 28.8687673678 * x))
    elif x < -0.15:
        return 0.871037573309 + x * (-0.634232323039 + x * (-18.4536797861 - 15.1329387029 * x))
    elif x < 0.15:
        x2 = x * x
        return 0.90154267737 + x2 * (-13.6879509584 + 16.7397805313 * x2)
    elif x < 0.25:
        return 0.871037573309 + x * (0.634232323039 + x * (-18.4536797861 + 15.1329387029 * x))
    elif x < 0.35:
        return 0.645147736088 + x * (3.29984031237 + x * (-28.9358315141 + 28.8687673678 * x))
    elif x < 0.4:
        return -0.242340474369 + x * (11.0004026851 + x * (-51.2046399185 + 50.3316340626 *x))
    elif x < 0.45:
        return -2.72415704125 + x * (29.4601745573 + x * (-96.9694386506  + 88.148440549 * x))
    elif x < 0.485:
        return -14.4841833281 + x * (107.462486507 + x * (-269.423768994 + 215.237469947 * x))
    else:
        return -141.683313066 + x * (890.871247193 + x * (-1877.70991482 + 1315.78489017 * x))


cubc = cub_complement


def qua(phase):
    x = phase - floor(phase + 0.5)
    x2 = x * x
    return 0.875 - x2 * (15 - 30 * x2)


def qui(phase):
    x = phase - floor(phase + 0.5)
    x2 = x * x
    return x * (5.96255602510703402 - x2 * (34.0717487148973373 - 40.8860984578768047 * x2))


def sex(phase):
    x = phase - floor(phase + 0.5)
    x2 = x * x
    return -0.96875 + x2 * (18.375 + x2 * (42 * x2 - 52.5))


def sep(phase):
    x = phase - floor(phase + 0.5)
    x2 = x * x
    return x * (x2 * (39.164736561902885 + x2 * (38.365456223904864 * x2 - 67.13954839183351)) - 6.19442261948464)


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
    return (hypot((1 + sharpness) * cos(pi * phase), (1 - sharpness) * sin(pi * phase)) - 1) / sharpness


def softtriangle(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - epsilon)
    return asin(s * sin(x)) / asin(s)


pi_squared = pi * pi
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
    return func(phase) - func(phase + bias)


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
