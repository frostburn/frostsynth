from math import floor


class PolyTable(list):
    def __init__(self, coefficientss, periodic=False, shift=0):
        super().__init__(coefficientss)
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

    def dc_block(self):
        dc = 0.0
        for coefficients in self:
            for i, coefficient in enumerate(reversed(coefficients)):
                dc += coefficient / (i + 1)

        correction = -dc / len(self)
        for index, coefficients in enumerate(self[:]):
            t = type(coefficients)
            self[index] = coefficients[:-1] + t([coefficients[-1] + correction])

    def differentiate(self):
        """Only works correctly for continuous data."""
        for index, coefficients in enumerate(self[:]):
            new_coefficients = []
            for i, coefficient in enumerate(reversed(coefficients)):
                new_coefficients.insert(0, coefficient * i)
            self[index] = tuple(new_coefficients[:-1])

    def integrate(self):
        """Only works correctly if DC blocked first."""
        dc = 0.0
        for index, coefficients in enumerate(self[:]):
            new_coefficients = []
            for i, coefficient in enumerate(reversed(coefficients)):
                new_coefficients.insert(0, coefficient / (i + 1))
            new_coefficients.append(dc)
            dc = sum(new_coefficients)
            self[index] = tuple(new_coefficients)


class ConstantTable(PolyTable):
    def __init__(self, data, periodic=False):
        coefficients = [(datum,) for datum in data]
        super().__init__(coefficients, periodic=periodic)


class LinearTable(PolyTable):
    def __init__(self, data, periodic=False):
        coefficientss, shift = self._calculate_coefficientss(list(data), periodic)
        super().__init__(coefficientss, periodic=periodic, shift=shift)

    def _calculate_coefficientss(self, data, periodic):
        if periodic:
            data = data + data[:1]
            shift = 0
        else:
            t = type(data)
            data = t([0.0]) + data + t([0.0])
            shift = 1
        coefficientss = []
        for d0, d1 in zip(data, data[1:]):
            coefficientss.append((d1 - d0, d0))
        return coefficientss, shift


class CubicTable(LinearTable):
    def _calculate_coefficientss(self, data, periodic):
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


class WaveForm(SplineTable):
    def __init__(self, data, tension=0.5):
        super().__init__(data=data, periodic=True, tension=tension)

    def __call__(self, phase):
        return super().__call__(phase * len(self))

    def differentiate(self):
        for index, coefficients in enumerate(self[:]):
            self[index] = tuple(coefficient * len(self) for coefficient in coefficients)

    def integrate(self):
        self.dc_block()
        super().integrate()
        i_len = 1.0 / len(self)
        for index, coefficients in enumerate(self[:]):
            self[index] = tuple(coefficient * i_len for coefficient in coefficients)
