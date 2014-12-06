from random import random


def quantize(source, steps=32767):
    """
    Quantize signal so that there are N steps in the unit interval.
    """
    i_steps = 1.0 / steps
    return [round(sample * steps) * i_steps for sample in source]


def dither(source, steps=32767):
    """
    Apply triangular dither.
    Goes well with quantize() with the same steps value.
    """
    i_steps = 1.0 / steps
    scale = 1.0 - i_steps
    return [sample * scale + i_steps * (random() - random()) for sample in source]
