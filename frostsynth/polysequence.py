class PolySequence(object):
    def __init__(self, xs, coefficientss, periodic=False):
        self.xs = xs
        self.coefficientss = coefficientss
        self.periodic = periodic

    def __call__(self, x):
        if self.periodic:
            raise NotImplemented
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
                r = 0.0
                for coefficient in coefficients:
                    r = mu * r + coefficient
                return r


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
            yield (next(l), next(l))
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
