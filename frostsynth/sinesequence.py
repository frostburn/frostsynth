from math import pi, cos, sin

from frostsynth import i_pi, i_two_pi


class SineSpline(object):
    def __init__(self, data, periodic=False, srate=None):
        xs, ys, ms = zip(*data)
        scales = []
        coefficientss = []
        for x0, x1, y0, y1, m0, m1 in zip(xs, xs[1:], ys, ys[1:], ms, ms[1:]):
            l = x1 - x0
            if l <= 0:
                scales.append(0)
                coefficientss.append((y0, 0, 0, 0))
            else:
                scales.append(pi / l)
                l *= i_two_pi
                coefficientss.append((0.5 * (y0 + y1), 0.5 * (y0 - y1), l * (m0 - m1), l * (m0 + m1)))
        self.xs = xs
        self.scales = scales
        self.coefficientss = coefficientss
        self.periodic = periodic
        self.srate = srate

    def __call__(self, x):
        if self.periodic:
            raise NotImplementedError
        else:
            if x < self.xs[0]:
                return 0
            elif x >= self.xs[-1]:
                return 0
            else:
                for index, next_sx in enumerate(self.xs, -1):
                    if x < next_sx:
                        break
                    sx = next_sx
                a, b, c, d = self.coefficientss[index]
                mu = (x - sx) * self.scales[index]
                s = sin(mu)
                return a + (b + d * s) * cos(mu) + c * s

    @classmethod
    def from_points(cls, data):
        xs, ys = zip(*data)
        ms = [(xs[1] - xs[0]) / (ys[1] - ys[0])]
        for x0, x1, x2, y0, y1, y2 in zip(xs, xs[1:], xs[2:], ys, ys[1:], ys[2:]):
            ms.append(2 * ((x1 - x0) / (y1 - y0) + (x2 - x1) / (y2 - y1)))
        ms.append((xs[-1] - xs[-2]) / (ys[-1] - ys[-2]))
        return cls(zip(xs, ys, ms))

    # TODO:
    #@classmethod
    #def natural_from_points(cls, data):
    #    pass