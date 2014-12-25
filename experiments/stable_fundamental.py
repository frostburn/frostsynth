def fundamental_optima(f, n=1, N=1000, lattice_constant=0.001, resolution=0.01, iterations=100):
    i_N = 1 / N
    n_two_pi_per_N = n * two_pi / N
    fundamental = lambda x: sum(sin(n_two_pi_per_N * i) * f(i * i_N, x) for i in range(N))
    return optima(fundamental, lattice_constant=lattice_constant, resolution=resolution, iterations=iterations)


class StableFundamental(object):
    def __init__(self, func, n=1):
        self.func = func
        self.optima = RandomAccessIterator(fundamental_optima(func, n=n))

    def __call__(self, phase, timbre):
        h = 0
        sign = -1
        for optimum in self.optima:
            sign = -sign
            l = h
            h = optimum
            if h > timbre:
                break
        mu = (timbre - l) / (h - l)
        return self.func(phase, l) * (1 - mu) * sign - self.func(phase, h) * mu * sign
