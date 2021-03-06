from cmath import log as clog, atanh as catanh

from frostsynth import epsilon


def constant_series(z):
    """
    returns 1 + z + z ** 2 + ...
    """
    return 1 / (1 - z)


def constant_series_n(z, n):
    """
    returns 1 + z + z ** 2 + ... + z ** n
    """
    z1 = 1 - z
    if abs(z1) < epsilon:
        return n + 1
    return (1 - z ** (n + 1)) / z1


def linear_series(z, a, delta):
    """
    returns a + (a + delta) * z + (a + 2 * delta) * z ** 2 + ...
    """
    z1 = 1 - z
    return (a - (a + delta) * z) / (z1 * z1)


def linear_series_n(z, a, b, n):
    """
    returns a + i1 * z + i2 * z ** 2 + b * z ** n, where the i coefficients interpolate between a and b.
    """
    zn = z ** n
    bzn = b * zn
    zn1 = 1 - zn
    z1 = 1 - z
    nz1 = n * z1
    zzn1 = z * zn1
    if abs(z1) < epsilon:
        return 0.5 * (a + b) * (1 + n)
    return ((b - a) * zzn1 + nz1 * (a - z * bzn)) / (nz1 * z1)


def quadratic_series(z, a, delta1, delta2):
    """
    returns a + (a + delta1 + delta2) * z + (a + 2 * delta1 + 4 * delta2) * z ** 2 + ....
    """
    z1 = 1 - z
    z1z1 = z1 * z1
    return (a * z1z1 + z * (delta1 + delta2 - (delta2 - delta1) * z)) / (z1 * z1z1)


def power_series(z, cs):
    """
    returns cs[0] + cs[1] * z + cs[2] * z ** 2 + ... + cs[-1] * z ** (len(cs) - 1)
    """
    s = cs[-1]
    for c in reversed(cs[:-1]):
        s *= z
        s += c
    return s


def harmonic_series(z):
    """
    returns z + z ** 2 / 2 + z ** 3 / 3 + ...
    """
    z1 = 1 - z
    if z1 == 0:
        return 0
    return -clog(z1)


def biharmonic_series(z):
    """
    returns sum(z ** k / (k * (1 + k)) for k in count(1))
    """
    if z == 0:
        return 0
    z1 = 1 - z
    if z1 == 0:
        return 1
    return 1 + (1/z - 1) * clog(z1)


def triharmonic_series(z):
    """
    returns 4 * sum(z ** k / (k * (1 + k) * (2 + k)) for k in count(1))
    """
    if z == 0:
        return 0
    z1 = 1 - z
    if z1 == 0:
        return 1
    zz = z * z
    term = z1 * z1 * clog(z1)
    return (zz + zz + zz - z - z - term - term) / zz


def demiharmonic_series(z):
    """
    returns sum(z ** (2 * k) / (2 * k * (k + 1/2)) for k in count(1))
    """
    zz1 = 1 - z * z
    if z == 0:
        return 0
    if zz1 == 0:
        return 2 - clog(4)
    return (2 * z - 2 * catanh(z) - z * clog(zz1)) / z
