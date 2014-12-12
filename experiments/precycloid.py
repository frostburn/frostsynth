from math import *

two_pi = 2 * pi

i_two_pi = 1 / two_pi

epsilon = 1e-12

PRECYCLOID_MAX_ITERATIONS = 5

def _precycloid_m1(x, a):
    t = 1.8171205928321397 * x ** 0.3333333333333333 + 0.1 * x
    for _ in range(PRECYCLOID_MAX_ITERATIONS):
        old_t = t
        t -= (t + a * sin(t) - x) / (1 + a * cos(t))
        if abs(t - old_t) < epsilon:
            break
    return t

def _precycloid(x, a):
    if x < 3.1:
        i_a1 = 1 / (1 + a)
        x_i_a1 = x * i_a1
        y = x_i_a1 * x_i_a1 * i_a1
        t = x_i_a1 * (1 + y * (a * 0.16666666666666666 + y * (a * (a * 9 - 1) * 0.008333333333333333 + y * (a * (1 - a * (54 - a * 225))) * 0.0001984126984126984)))
    else:
        t = x
    for _ in range(PRECYCLOID_MAX_ITERATIONS):
        old_t = t
        t -= (t + a * sin(t) - x) / (1 + a * cos(t))
        if abs(t - old_t) < epsilon:
            break
    return t

def precycloid(x, a=-1.0):
    """Returns t such that x = t + a * sin(t)"""
    if x == 0:
        return 0.0
    elif x < 0 or x > two_pi:
        return floor(x * i_two_pi) * two_pi + precycloid(x % two_pi, a)
    elif x > pi:
        return two_pi - precycloid(two_pi - x, a)
    elif a < -0.9 and x < 0.1:
        return _precycloid_m1(x, a)
    elif a > 0.9 and x > 3.04:
        return pi - _precycloid_m1(pi - x, -a)
    elif a < 0:
        return pi - _precycloid(pi - x, -a)
    else:
        return _precycloid(x, a)


from random import *
l = []
for i in range(10000000):
    x = random() * two_pi
    a = random() * 2 - 1
    t = precycloid(x, a)
    l.append(abs(t + a * sin(t) - x))

print(max(l))
