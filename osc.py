from math import *

clip = lambda a, a_min, a_max: a_min if a < a_min else (a_max if a > a_max else a)

epsilon = 1e-10

def softsaw(p, sharpness):
    x = 2 * pi * p
    s = clip(sharpness, epsilon, 1 - epsilon)
    return atan(s * sin(x) / (1.0 + s * cos(x))) / asin(s)
