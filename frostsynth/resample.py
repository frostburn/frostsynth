from frostsynth import *

from frostsynth.interpolation import *


def resampler0_gen(source, ratio):
    """Dynamic resampling of 'source' by variable ratio. Constant interpolation."""
    ratio = to_iterable(ratio)

    sample = next(source)
    index = 0.0
    source_index = 1
    while True:
        yield sample
        index += next(ratio)
        while source_index <= index:
            sample = next(source)
            source_index += 1


def resampler1_gen(source, ratio):
    """Dynamic resampling of 'source' by variable ratio. First order interpolation."""
    source = chain(source, [0.0])
    ratio = to_iterable(ratio)

    index = 0.0
    sample0 = next(source)
    sample1 = next(source)
    source_index = 1
    while True:
        yield sample0 + (sample1 - sample0) * (index + 1 - source_index)
        index += next(ratio)
        while source_index <= index:
            sample0 = sample1
            sample1 = next(source)
            source_index += 1


def resampler3_gen(source, ratio):
    """Dynamic resampling of 'source' by variable ratio. Third order Lagrange interpolation."""
    source = chain(source, [0.0, 0.0])
    ratio = to_iterable(ratio)

    index = 0.0
    sample0 = 0.0
    sample1 = next(source)
    sample2 = next(source)
    sample3 = next(source)
    source_index = 1
    while True:
        yield lagrange_four_point(index + 1 - source_index, sample0, sample1, sample2, sample3)
        index += next(ratio)
        while source_index <= index:
            sample0 = sample1
            sample1 = sample2
            sample2 = sample3
            sample3 = next(source)
            source_index += 1


def analytic_resample1(f, frequency, sub_samples=1, variability=0, srate=None):
    dt = 1 / get_srate(srate)
    ratio = 1 / sub_samples
    frequency = to_iterable(frequency)
    y1 = f(0)
    target = 0
    phase = target
    for sample in frequency:
        if phase >= target:
            y0 = y1
            y1 = f(phase)
            prev_target = target
            d_target = (1.0 + (random() - 0.5) * variability) * ratio
            target += d_target
            dp = (y1 - y0) / d_target
        yield y0 + dp * (phase - prev_target)
        phase += sample * dt
