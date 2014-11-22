from math import floor


class PolyTable(list):
    def __init__(self, coefficients, periodic=False, shift=0):
        super().__init__(coefficients)
        self.periodic = periodic
        self.shift = shift

    def __call__(self, x):
        index = int(floor(x))
        mu = x - index
        index += self.shift
        if self.periodic:
            index %= len(self)
        elif index < 0:
            return 0.0
        elif index >= len(self):
            return 0.0
        r = 0.0
        for coefficient in self[index]:
            r = mu * r + coefficient
        return r


class LinearTable(PolyTable):
    def __init__(self, data, periodic=False):
        coefficients, shift = self._calculate_coefficients(data, periodic)
        super().__init__(coefficients, periodic=periodic, shift=shift)

    def _calculate_coefficients(self, data, periodic):
        if periodic:
            data = data + data[:1]
            shift = 0
        else:
            t = type(data)
            data = t([0.0]) + data + t([0.0])
            shift = 1
        coefficients = []
        for d0, d1 in zip(data, data[1:]):
            coefficients.append((d1 - d0, d0))
        return coefficients, shift


class CubicTable(LinearTable):
    def _calculate_coefficients(self, data, periodic):
        if periodic:
            data = data + data[:1]
            shift = 0
        else:
            t = type(data)
            data = t([(0.0, 0.0)]) + data + t([(0.0, 0.0)])
            shift = 1
        coefficientss = []
        for d0, d1 in zip(data, data[1:]):
            coefficients = (
                2 * (d0[0] - d1[0]) + d0[1] + d1[1],
                3 * (d1[0] - d0[0]) - d0[1] - d0[1] - d1[1],
                d0[1],
                d0[0],
            )
            coefficientss.append(coefficients)
        return coefficientss, shift


class SplineTable(CubicTable):
    def __init__(self, data, periodic=False, tension=0.5):
        if periodic:
            data = data[-1:] + data + data[:1]
        else:
            t = type(data)
            data = t([0.0, 0.0]) + data + t([0.0, 0.0])

        segment_data = []
        for d0, d1, d2 in zip(data, data[1:], data[2:]):
            segment_data.append((d1, 0.5 * (1 - tension) * (d2 - d0)))
        super().__init__(segment_data, periodic=periodic)
        if not periodic:
            self.shift = 2
