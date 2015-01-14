from math import ceil

from frostsynth import get_srate


class PolySequence(object):
    def __init__(self, xs, coefficientss, periodic=False, srate=None):
        self.xs = xs
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
                sx = self.xs[0]
                for index, next_sx in enumerate(self.xs, -1):
                    if x < next_sx:
                        break
                    sx = next_sx
                coefficients = self.coefficientss[index]
                mu = x - sx
                r = 0
                for coefficient in coefficients:
                    r = mu * r + coefficient
                return r

    def __iter__(self):
        srate = get_srate(self.srate)
        dt = 1 / srate
        x = self.xs[0]
        prev_x = x
        for i, target_x in enumerate(self.xs[1:]):
            dx = x - prev_x
            if dx < 0:
                continue
            samples = int(ceil((target_x - x) * srate))
            coefficients = self.coefficientss[i]
            if not coefficients:
                for _ in range(samples):
                    yield 0
            elif len(coefficients) == 1:
                coef = coefficients[0]
                for _ in range(samples):
                    yield coef
            elif len(coefficients) == 2:
                accumulator = coefficients[1] + coefficients[0] * dx
                yield accumulator
                da = coefficients[0] * dt
                for _ in range(samples - 1):
                    accumulator += da
                    yield accumulator
            elif len(coefficients) == 3:
                accumulator0 = coefficients[2] + (coefficients[1] + coefficients[0] * dx) * dx
                yield accumulator0
                da = coefficients[0] * dt * dt
                accumulator1 = (coefficients[1] + 2 * dx * coefficients[0]) * dt - da
                da += da
                for _ in range(samples - 1):
                    accumulator1 += da
                    accumulator0 += accumulator1
                    yield accumulator0
            elif len(coefficients) == 4:
                accumulator0 = coefficients[3] + (coefficients[2] + (coefficients[1] + coefficients[0] * dx) * dx) * dx
                yield accumulator0
                dt2 = dt * dt
                dxdt = dx * dt
                da = coefficients[0] * dt2 * dt
                b = coefficients[1] * dt2
                accumulator1 = coefficients[2] * dt - b + da + (2 * coefficients[1] * dt + 3 * coefficients[0] * (dxdt - dt2)) * dx
                da *= 6
                accumulator2 = b + b - da + 6 * coefficients[0] * dxdt * dt
                for _ in range(samples - 1):
                    accumulator2 += da
                    accumulator1 += accumulator2
                    accumulator0 += accumulator1
                    yield accumulator0
            else:
                t = x
                for _ in range(samples):
                    yield self(t)
                    t += dt
            x += samples * dt
            prev_x = target_x

    def extend_to(self, value=0):
        if value < self.xs[0]:
            self.xs.insert(0, value)
            self.coefficientss.insert(0, ())
        elif value > self.xs[-1]:
            self.xs.append(value)
            self.coefficientss.append(())

    def extend(self, other):
        delta_x = self.xs[-1] - other.xs[0]
        self.xs[-1:] = [x + delta_x for x in other.xs]
        self.coefficientss.extend(other.coefficientss)

    def scale_y(self, multiplier):
        self.coefficientss = [tuple(multiplier * coefficient for coefficient in coefficients) for coefficients in self.coefficientss]

    def scale_x(self, multiplier):
        self.xs = [multiplier * x for x in self.xs]
        self.coefficientss = [tuple(multiplier ** (i - len(coefficients) + 1) * coefficient for i, coefficient in enumerate(coefficients)) for coefficients in self.coefficientss]

    def differentiate(self):
        self.coefficientss = [tuple(coefficient * (len(coefficients) - 1 - i) for i, coefficient in enumerate(coefficients[:-1])) for coefficients in self.coefficientss]

    def integrate(self):
        dc = 0
        for index, coefficients in enumerate(self.coefficientss[:]):
            delta_x = self.xs[index + 1] - self.xs[index]
            new_coefficients = []
            for i, coefficient in enumerate(reversed(coefficients)):
                new_coefficients.insert(0, coefficient / (i + 1))
            new_coefficients.append(dc)
            dc = sum(coefficient * delta_x ** i for i, coefficient in enumerate(reversed(new_coefficients)))
            self.coefficientss[index] = tuple(new_coefficients)

    @classmethod
    def constant(_, duration, value, start=0):
        return PolySequence([start, start + duration], [(value,)])


class LinearSequence(PolySequence):
    def __init__(self, data):
        coefficientss = []
        for d0, d1 in zip(data, data[1:]):
            l = (d1[0] - d0[0])
            if l > 0:
                coefficientss.append(((d1[1] - d0[1]) / l, d0[1]))
            else:
                coefficientss.append((d0[1],))
        super().__init__([d[0] for d in data], coefficientss)

    @classmethod
    def from_flat_list(cls, l):
        def g():
            i = iter(l)
            while True:
                yield (next(i), next(i))
        return cls(list(g()))


class CubicSequence(PolySequence):
    def __init__(self, data, smooth=False):
        xs = []
        coefficientss = []
        for d0, d1 in zip(data, data[1:]):
            x0 = d0[0]
            x1 = d1[0]
            l = (x0 - x1)
            if l < 0:
                y0 = d0[1]
                s0 = d0[3]

                y1 = d1[1]
                s1 = d1[2]

                a = ((s0 + s1) * (x0 - x1) - 2 * y0 + 2 * y1) / l ** 3
                b = ((2 * s0 + s1) * l - 3 * y0 + 3 * y1) / l ** 2
                coefficientss.append((a, b, s0, y0))
            else:
                coefficientss.append((d0[1],))
            xs.append(x0)
        xs.append(data[-1][0])
        super().__init__(xs, coefficientss)

    @classmethod
    def from_flat_bezier(cls, l):
        d0 = l[2] - l[0]
        s0 = (l[3] - l[1]) / d0 if d0 != 0 else 0
        data = [(l[0], l[1], None, s0)]
        i = 6
        while i + 3 < len(l):
            d1 = l[i] - l[i - 2]
            s1 = (l[i + 1] - l[i - 1]) / d1 if d1 != 0 else 0
            d0 = l[i + 2] - l[i]
            s0 = (l[i + 3] - l[i + 1]) / d0 if d0 != 0 else 0
            data.append((l[i], l[i + 1], s1, s0))
            i += 6
        d1 = l[-2] - l[-4]
        s1 = (l[-1] - l[-3]) / d1 if d1 != 0 else 0
        data.append((l[-2], l[-1], s1))
        return cls(data)
