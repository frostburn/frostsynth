from math import *
from cmath import exp as cexp

from frostsynth import epsilon, clip, two_pi, two_pi_j, i_pi

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


def softtriangle(phase, sharpness):
    x = two_pi * phase
    s = clip(sharpness, epsilon, 1 - epsilon)
    return asin(s * sin(x)) / asin(s)


pi_squared = pi * pi


def theta(phase, sharpness):
    """DC-blocked peak-amplitude normalized EllipticTheta(3, pi * phase, sharpness)"""
    q = sharpness
    if q < epsilon:
        return cos(two_pi * phase)
    elif q < 0.2:
        coefs = [q ** (n * n) for n in range(1, 6)]
        return sum(c * cos(two_pi * n * phase) for n, c in enumerate(coefs, 1)) / sum(coefs)
    elif q < 1:
        x = phase - floor(phase + 0.5)
        i_log_q = 1 / log(q)
        a = pi_squared * i_log_q
        b = 0.5 * sqrt(-pi * i_log_q)
        return (sum(exp(a * (x - n) * (x - n)) for n in range(-2 , 3)) * b - 0.5) / ((1 + 2 * (exp(a) + exp(4 * a))) * b - 0.5)
    else:
        return 0.0


def theta_rect(phase, sharpness):
    """Peak-amplitude normalized EllipticTheta(3, pi * phase, sharpness)"""
    q = sharpness
    if q < epsilon:
        return 0.5 * 0.5 * cos(two_pi * phase)
    elif q < 0.2:
        coefs = [q ** (n * n) for n in range(1, 6)]
        return (1 + sum(c * cos(two_pi * n * phase) for n, c in enumerate(coefs, 1))) / (1 + sum(coefs))
    elif q < 1:
        x = phase - floor(phase + 0.5)
        a = pi_squared / log(q)
        return sum(exp(a * (x - n) * (x - n)) for n in range(-2 , 3)) / (1 + 2 * (exp(a) + exp(4 * a)))
    else:
        return 0.0


def sine(phase):
    return sin(two_pi * phase)


def cosine(phase):
    return cos(two_pi * phase)


def rsine(phase, vmin=0.0, vmax=1.0):
   return vmin  + (sin(two_pi * phase) + 1) * 0.5 * (vmax - vmin)


def rcosine(phase, vmin=0.0, vmax=1.0):
   return vmin  + (cos(two_pi * phase) + 1) * 0.5 * (vmax - vmin)


def cis(phase):
    return cexp(two_pi_j * phase)


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
