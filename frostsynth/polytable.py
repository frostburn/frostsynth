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
            data += data[:1]
            shift = 0
        else:
            data = [0.0] + data + [0.0]
            shift = 1
        coefficientss = []
        for d0, d1 in zip(data, data[1:]):
            coefficientss.append((d1 - d0, d0))
        return coefficientss, shift


class CubicTable(LinearTable):
    def _calculate_coefficientss(self, data, periodic):
        if periodic:
            data += data[:1]
            shift = 0
        else:
            data = [(0.0, 0.0)] + data + [(0.0, 0.0)]
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


class PolyTableComplex(object):
    def __init__(self, coefficientss, len_real, shift_real=0, shift_imag=0):
        if len(coefficientss) % len_real:
            raise ValueError("Only rectangular data supported")
        self._coefficientss = coefficientss
        self._len_real = len_real
        self._len_imag = len(coefficientss) // len_real
        self.shift_real = shift_real
        self.shift_imag = shift_imag

    @property
    def len_real(self):
        return self._len_real

    @property
    def len_imag(self):
        return self._len_imag

    def __getitem__(self, coords):
        return self._coefficientss[coords[0] + self._len_real * coords[1]]

    def __call__(self, z):
        index_real = int(floor(z.real))
        index_imag = int(floor(z.imag))
        mu = z - index_real - index_imag * 1j
        index_real += self.shift_real
        index_imag += self.shift_imag
        if index_real < 0:
            return 0.0
        elif index_imag < 0:
            return 0.0
        elif index_real >= self._len_real:
            return 0.0
        elif index_imag >= self._len_imag:
            return 0.0
        r = 0.0j
        for coefficient in self[index_real, index_imag]:
            r = mu * r + coefficient
        return r


class PolyTable2D(object):
    def __init__(self, coefficientss, len_x, periodic_x=False, periodic_y=False, shift_x=0, shift_y=0):
        if len(coefficientss) % len_x:
            raise ValueError("Only rectangular data supported")
        self._coefficientss = coefficientss
        self._len_x = len_x
        self._len_y = len(coefficientss) // len_x
        self.periodic_x = periodic_x
        self.periodic_y = periodic_y
        self.shift_x = shift_x
        self.shift_y = shift_y

    @property
    def len_x(self):
        return self._len_x

    @property
    def len_y(self):
        return self._len_y

    def __getitem__(self, coords):
        return self._coefficientss[coords[0] + self._len_x * coords[1]]

    def __call__(self, x, y):
        index_x = int(floor(x))
        index_y = int(floor(y))
        mu_x = x - index_x
        mu_y = y - index_y
        index_x += self.shift_x
        index_y += self.shift_y
        if self.periodic_x:
            index_x %= self._len_x
        elif index_x < 0:
            return 0.0
        elif index_x >= self._len_x:
            return 0.0
        if self.periodic_y:
            index_y %= self._len_y
        elif index_y < 0:
            return 0.0
        elif index_y >= self._len_y:
            return 0.0
        r = 0.0
        for coefficients in self[index_x, index_y]:
            rx = 0.0
            for coefficient in coefficients:
                rx = mu_x * rx + coefficient
            r = mu_y * r + rx
        return r


class LinearTable2D(PolyTable2D):
    def __init__(self, data, periodic_x=False, periodic_y=False):
        data = [list(data_x) for data_x in data]
        len_x = len(data[0])
        if not all(len(data_x) == len_x for data_x in data):
            raise ValueError("Only rectangular data supported")
        coefficientss, shift_x, shift_y = self._calculate_coefficientss(data, periodic_x, periodic_y)
        len_x += shift_x
        super().__init__(coefficientss, len_x, periodic_x=periodic_x, periodic_y=periodic_y, shift_x=shift_x, shift_y=shift_y)

    def _calculate_coefficientss(self, data, periodic_x, periodic_y):
        if periodic_x:
            data = [data_x + data_x[:1] for data_x in data]
            shift_x = 0
        else:
            data = [[0.0] + data_x + [0.0] for data_x in data]
            shift_x = 1
        if periodic_y:
            data += data[1:]
            shift_y = 0
        else:
            len_x = len(data[0])
            data = [[0.0] * len_x] + data + [[0.0] * len_x]
            shift_y = 1
        coefficientss = []
        for data_x0, data_x1 in zip(data, data[1:]):
            for d00, d10, d01, d11 in zip(data_x0, data_x0[1:], data_x1, data_x1[1:]):
                coefficientss.append(((d11 - d10 - d01 + d00 , d01 - d00), (d10 - d00, d00)))
        return coefficientss, shift_x, shift_y


class XCubicTable2D(LinearTable2D):
    def _calculate_coefficientss(self, data, periodic_x, periodic_y):
        if periodic_x:
            data = [data_x + data_x[:1] for data_x in data]
            shift_x = 0
        else:
            data = [[(0.0, 0.0)] + data_x + [(0.0, 0.0)] for data_x in data]
            shift_x = 1
        if periodic_y:
            data += data[1:]
            shift_y = 0
        else:
            len_x = len(data[0])
            data = [[(0.0, 0.0)] * len_x] + data + [[(0.0, 0.0)] * len_x]
            shift_y = 1
        coefficientss = []
        for data_x0, data_x1 in zip(data, data[1:]):
            for d00, d10, d01, d11 in zip(data_x0, data_x0[1:], data_x1, data_x1[1:]):
                a0 = 2 * (d00[0] - d10[0]) + d00[1] + d10[1]
                a1 = 2 * (d01[0] - d11[0]) + d01[1] + d11[1]
                b0 = 3 * (d10[0] - d00[0]) - d00[1] - d00[1] - d10[1]
                b1 = 3 * (d11[0] - d01[0]) - d01[1] - d01[1] - d11[1]
                c0 = d00[1]
                c1 = d01[1]
                d0 = d00[0]
                d1 = d01[0]
                coefficientss.append((
                    (a1 - a0, b1 - b0, c1 - c0, d1 - d0),
                    (a0, b0, c0, d0),
                ))
        return coefficientss, shift_x, shift_y
