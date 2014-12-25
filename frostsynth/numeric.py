from frostsynth import epsilon


def zeros(f, resolution=0.01, iterations=100):
    t0 = 0
    f0 = f(t0)
    if abs(f0) < epsilon:
        yield 0
    t1 = resolution
    f1 = f(t1)
    while True:
        while f0 * f1 >= 0:
            t0 = t1
            f0 = f1
            t1 += resolution
            f1 = f(t1)
        for _ in range(iterations):
            midpoint = (t1 + t0) * 0.5
            fm = f(midpoint)
            if f0 * fm < 0:
                t1 = midpoint
                f1 = fm
            else:
                t0 = midpoint
                f0 = fm
        yield (t1 + t0) * 0.5
        t0 = t1
        f0 = f1
        t1 += resolution
        f1 = f(t1)


def optima(f, lattice_constant=epsilon, resolution=0.01, iterations=100):
    lattice_constant *= 0.5
    return zeros(lambda x: f(x + lattice_constant) - f(x - lattice_constant), resolution=resolution, iterations=iterations)
