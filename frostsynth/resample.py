from itertools import *

from frostsynth.interpolation import *


def resampler1_gen(source, ratio):
    """Dynamic resampling of 'source' by variable ratio. First order interpolation."""
    source = chain(source, [0.0])
    ratio = iter(ratio)

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
    ratio = iter(ratio)

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
