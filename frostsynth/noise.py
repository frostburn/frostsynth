from random import *
from random import gauss as random_gauss
from cmath import rect as from_polar
from math import sqrt, cos

from frostsynth import *
from frostsynth.interpolation import *
from frostsynth.ffi import uniform as fast_uniform
from frostsynth.polysequence import LinearSequence, NaturalSpline


def fast_uniform_t(duration, srate=None):
    srate = get_srate(srate)
    return fast_uniform(int(duration * srate))


def uniform_gen(vmin=-1.0, vmax=1.0):
    """Generate uniform noise in the range from vmin to vmax."""
    if vmin == 0.0 and vmax == 1.0:
        while True:
            yield random()
    else:
        scale = vmax - vmin
        while True:
            yield random() * scale + vmin


def uniform(k=None, vmin=-1.0, vmax=1.0):
    """Generate uniform noise in the range from vmin to vmax."""
    if vmin == 0.0 and vmax == 1.0:
        if k is None:
            return random()
        else:
            return [random() for _ in range(k)]
    else:
        scale = vmax - vmin
        if k is None:
            return random() * scale + vmin
        else:
            return [random() * scale + vmin for _ in range(k)]


def uniform_t(duration, vmin=-1.0, vmax=1.0, srate=None):
    srate = get_srate(srate)
    return uniform(int(duration * srate), vmin=vmin, vmax=vmax)


def gauss(k=None, mu=0, sigma=1):
    if k is None:
        return random_gauss(mu, sigma)
    else:
        return [random_gauss(mu, sigma) for _ in range(k)]


def cunit(k=None):
    if k is None:
        return from_polar(1, two_pi * random())
    else:
        return [from_polar(1, two_pi * random()) for _ in range(k)]


def cunit_t(duration, srate=None):
    srate = get_srate(srate)
    return cunit(int(duration * srate))


def pink_gen(octaves=16):
    """
    Generates a sum of successive octaves of white noise to create approximate pink noise.

    Normalized to have unit variance.
    """
    shift = -0.5 * octaves
    scale = sqrt(12.0 / octaves)
    values = [random() for _ in range(octaves)]
    for i in count():
        # Each value is updated in the middle of every 2 ** k:th step.
        values[0] = random()
        for j  in range(octaves - 1):
            if i & ((1 << (j + 1)) - 1) == 1 << j:
                values[j + 1] = random()
        yield (sum(values) + shift) * scale


def impulse_snow_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    """Impulse noise from vmin to vmax driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1 / srate
    frequency = to_iterable(frequency)

    target = 1.0
    phase = target
    while True:
        if phase >= target:
            yield uniform(vmin=vmin, vmax=vmax)
            phase %= target
            target = 1.0 + (random() - 0.5) * variability
        else:
            yield 0
        phase += dt * next(frequency)


def snow0_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    """Constant interpolated white noise from vmin to vmax driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1.0 / srate
    frequency = to_iterable(frequency)

    target = 1.0
    phase = target
    while True:
        if phase >= target:
            y0 = uniform(vmin=vmin, vmax=vmax)
            phase = phase % target
            target = 1.0 + (random() - 0.5) * variability
        yield y0
        phase += dt * next(frequency)


def snow1_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    """Linear interpolated white noise from vmin to vmax driven by 'frequency'."""
    srate = get_srate(srate)
    frequency = to_iterable(frequency)

    y1 = uniform(vmin=vmin, vmax=vmax)
    target = srate
    phase = target
    for sample in frequency:
        if phase >= target:
            y0 = y1
            y1 = uniform(vmin=vmin, vmax=vmax)
            phase = phase % target
            target = (1.0 + (random() - 0.5) * variability) * srate
            dp = (y1 - y0) / target
        yield y0 + dp * phase
        phase += sample


def _func_snow3_gen(func):
    def snow3_gen(frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
        """
        Cubic interpolated noise controlled by 'frequency'.

        Approximately withing range from vmin to vmax, but does overshoot.
        """
        srate = get_srate(srate)
        dt = 1.0 / srate

        frequency = to_iterable(frequency)

        y3 = uniform(vmin=vmin, vmax=vmax)
        y2 = uniform(vmin=vmin, vmax=vmax)
        y1 = uniform(vmin=vmin, vmax=vmax)
        target = 1.0
        phase = target
        while True:
            if phase >= target:
                y0 = y1
                y1 = y2
                y2 = y3
                y3 = uniform(vmin=vmin, vmax=vmax)
                phase = phase % target
                target = 1.0 + (random() - 0.5) * variability
                i_target = 1.0 / target
            yield func(phase * i_target, y0, y1, y2, y3)
            phase += dt * next(frequency)

    return snow3_gen


snow3_gen = _func_snow3_gen(lagrange_four_point)


snow3 = lambda frequency, vmin=-1.0, vmax=1.0, variability=0.0, srate=None: list(snow3_gen(frequency, vmin, vmax, variability, srate))


spline_snow_gen = _func_snow3_gen(catmull_rom_spline)


def sin_snow_gen(frequency, sharpness=0, vmin=-1.0, vmax=1.0, variability=0.0, srate=None):
    dt = 2 / get_srate(srate)
    frequency = to_iterable(frequency)
    sharpness = to_iterable(sharpness)

    y1 = uniform(vmin=vmin, vmax=vmax)
    phase = 2
    for f, s in zip(frequency, sharpness):
        if phase >= 2:
            y0 = y1
            y1 = uniform(vmin=vmin, vmax=vmax)
            d0 = 0.5 * (y0 + y1)
            d1 = 0.5 * (y1 - y0)
            phase = phase % 2
            target = 1 + (random() - 0.5) * variability
            dp = dt / target
        if phase <= s:
            yield y0
        elif phase >= 2 - s:
            yield y1
        else:
            p = half_pi * (phase - 1) / (1 - s)
            yield d0 + d1 * sin(p)
        phase += f * dp


def linear_noise(frequency, duration=None, srate=None):
    """Linear interpolated white noise with reduced spectral banding driven by 'frequency'."""
    srate = get_srate(srate)
    frequency = to_iterable_t(frequency, duration)
    y1 = 2 * random() - 1
    target = srate
    phase = srate
    result = []
    for sample in frequency:
        if phase >= target:
            phase = phase % target
            target = 0.5 + random()
            y0 = y1
            high = min(1, y0 + target * 1.2)
            low = max(-1, y0 - target * 1.2)
            y1 = (high - low) * random() + low
            target *= srate
            dp = (y1 - y0) / target
        result.append(y0 + dp * phase)
        phase += sample
    return result


def linear_noise2(frequency, srate=None):
    """Linear kernel white noise with reduced spectral banding driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1 / srate
    points = []
    next_x = 0
    for _ in range(5):
        w = 0.5 + random()
        y = random() - 0.5
        points.append((next_x, y, w))
        next_x += 0.5 + random()
    result = []
    phase = 0
    for sample in frequency:
        s = 0
        for index, (x, y, w) in enumerate(points):
            if phase > x + w:
                w = 0.5 + random()
                y = random() - 0.5
                points[index] = (next_x, y, w)
                next_x += 0.5 + random()
            elif phase > x:
                s += (w - phase + x) * y
            elif phase > x - w:
                s += (w - x + phase) * y
        result.append(s)
        phase += dt * sample
    return result


def parabolic_noise(frequency, duration=None, srate=None):
    """Interpolated white noise with approximately parabolic segments and reduced spectral banding driven by 'frequency'."""
    srate = get_srate(srate)
    dt = 1 / srate
    frequency = to_iterable_t(frequency, duration)
    y1 = 2 * random() - 1
    y2 = 2 * random() - 1
    v = y1 * 0
    target = srate
    phase = srate
    result = []
    for sample in frequency:
        if phase >= target:
            phase = phase % target
            target = 0.5 + random()
            y0, y1 = y1, y2
            high = min(1, y1 + target * 1.5)
            low = max(-1, y1 - target * 1.5)
            y2 = (high - low) * random() + low
            a = 5 * dt * (sample / target) ** 0.75
            target *= srate
            dv = a * (y1 - y0)
            dp = a * (y2 - y1 - y1 + y0) / target
        v = v * 0.995 + dv + dp * phase
        result.append(v)
        phase += sample
    return result


def quartic_noise(frequency, srate=None):
    srate = get_srate(srate)
    dt = 1 / srate
    points = []
    next_x = 0
    for _ in range(4):
        w = 0.5 + random()
        y = random() - 0.5
        points.append((next_x, y / w, w))
        next_x += 1
    result = []
    phase = 0
    for sample in frequency:
        s = 0
        for index, (x, y, w) in enumerate(points):
            if phase > x + w:
                w = 0.5 + random()
                y = random() - 0.5
                points[index] = (next_x, y / w, w)
                next_x += 1
            elif phase > x - w:
                p2 = (phase - x)
                p2 = w - p2 * p2 / w
                s += p2 * p2 * y
        result.append(s)
        phase += dt * sample
    return result


def cubic_noise(frequency, srate=None):
    srate = get_srate(srate)
    dt = 1 / srate
    points = []
    next_x = 0
    for _ in range(6):
        w = 0.7 + random() * 0.6
        y = random() - 0.5
        points.append((next_x, y * w, w))
        next_x += 0.45 + random() * 0.1
    result = []
    phase = 0
    for sample in frequency:
        s = 0
        for index, (x, y, w) in enumerate(points):
            if phase > x + w:
                w = 0.7 + random() * 0.6
                y = random() - 0.5
                points[index] = (next_x, y * w, w)
                next_x += 0.45 + random() * 0.1
            elif phase > x - w:
                p = 2 * abs(phase - x) / w
                if p < 1:
                    s += (1 + p * p * (p - 2)) * y
                else:
                    s += (4 + p * ((5 - p) * p - 8)) * y
        result.append(s)
        phase += dt * sample
    return result


def _smooth_noise_data(frequency, duration=None, variability=0, srate=None):
    srate = get_srate(srate)
    dt = 1 / srate
    frequency = to_iterable_t(frequency, duration, srate=srate)
    x = 0
    data = []
    r = 0
    target = 1
    phase = target
    try:
        while True:
            if phase >= target:
                high = min(1, r + target)
                low = max(-1, r - target)
                r = (high - low) * random() + low
                yield (x, r)
                phase %= target
                target = 1.0 + (random() - 0.5) * variability
            phase += dt * next(frequency)
            x += dt
    except StopIteration:
        pass
    high = min(1, x + target)
    low = max(-1, x - target)
    r = (high - low) * random() + low
    yield (x, r)


def smooth_noise(frequency, duration=None, variability=0.5, srate=None):
    return NaturalSpline(list(_smooth_noise_data(frequency, duration, variability, srate)))


def lpnoise_gen(bandwidth, order=2, srate=None):
    srate = get_srate(srate)
    bw = two_pi * bandwidth / srate
    bw2 = bw * bw
    d = 1 + (order * bw2 - bw * sqrt((4 + order * bw2) * order)) * 0.5
    d1 = 1 - d
    two_sqrt_d1 = 2 * sqrt(d1)
    y = [0.0] * order
    while  True:
        y[0] = two_sqrt_d1 * (random() - 0.5) + d * y[0]
        for i in range(order - 1):
            y[i + 1] = d1 * y[i] + d * y[i + 1]
        yield y[-1]


def dynamic_lpnoise_gen(bandwidth, order=2, srate=None):
    srate = get_srate(srate)
    m = two_pi / srate
    y = [0.0] * order
    for b in bandwidth:
        bw = m * b
        bw2 = bw * bw
        d = 1 + (order * bw2 - bw * sqrt((4 + order * bw2) * order)) * 0.5
        d1 = 1 - d
        y[0] = 2 * sqrt(d1) * (random() - 0.5) + d * y[0]
        for i in range(order - 1):
            y[i + 1] = d1 * y[i] + d * y[i + 1]
        yield y[-1]
