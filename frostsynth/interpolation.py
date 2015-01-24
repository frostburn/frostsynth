from math import pi, sin

from frostsynth import epsilon

def lagrange_four_point(x, y0, y1, y2, y3):
    """The third order polynomial p(x) with p(-1)=y0, p(0)=y1, p(1)=y2, p(2)=y3."""
    a2 = 3 * (y0 + y2 - y1 - y1)
    a3 = 3 * (y1 - y2) + y3 - y0
    a1 = -a3 + 3 * (y2 - y0)
    return y1 + x * (a1 + x * (a2 + x * a3)) * 0.166666666666666666666666


def catmull_rom_spline(x, y0, y1, y2, y3):
    """The third order polynomial p(x) with p(0)=y1, p'(0)=y2-y0, p(1)=y2, p'(1)=y3-y1."""
    a3 = y3 - y2 - y0 + y1
    a2 = y0 - y1 - a3
    return y1 + x * (y2 - y0 + x * (a2 + x * a3))


def cubic_hermite_spline(x, p0, m0, p1, m1):
    """The third order polynomial p(x) with p(0)=p0, p'(0)=m0, p(1)=p1, p'(1)=m1."""
    a3 = m0 + m1 + p0 + p0 - p1 - p1
    a2 =  p1 - a3 - m0 - p0
    return p0 + x * (m0 + x * (a2 + x * a3))


def sinc(x):
    """Single bandlimited impulse at 0. Suitable for bandlimited interpolation of sampled data."""
    x *= pi
    if abs(x) < epsilon:
        return 1 - x * x * 0.16666666666666666
    return sin(x) / x


def bl_interpolate(data, lowpass=1.0):
    """
    Returns a bandlimited function f(x) that gives the data points at values 0, 1, 2, ... but can be evaluated at any fractional point.
    Frequency cutoff is controlled by 'lowpass' in natural units: 0 ~ DC, 1 ~ sampling rate / 2.
    """
    if lowpass > 1.0:
        lowpass = 1.0
    def interpolant(x):
        return sum(datum * sinc((x - i) * lowpass) * lowpass for i , datum in enumerate(data))
    return interpolant
