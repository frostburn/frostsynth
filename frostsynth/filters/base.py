def onepole(source, a0, a1, b0):
    """One pole filter a0 y[n] = b0 x[n] - a1 y[n-1]."""
    source = iter(source)
    a1 = a1 / a0
    b0 = b0 / a0

    y0 = b0 * next(source)
    yield y0

    while True:
        y0 = b0 * next(source) - a1 * y0
        yield y0


def onezero(source, a0, b0, b1):
    """One zero filter a0 y[n] = b0 x[n] + b1 x[n-1]."""
    source = iter(source)
    b0 = b0 / a0
    b1 = b1 / a0

    x1 = next(source)
    yield b0 * x1

    while True:
        x0 = next(source)
        yield b0 * x0 + b1 * x1
        x1 = next(source)
        yield b0 * x1 + b1 * x0


def polezero(source, a0, a1, b0, b1):
    """One pole, one zero filter a0 y[n] = b0 x[n] + b1 x[n-1] - a1 y[n-1]."""
    source = iter(source)
    a1 = a1 / a0
    b0 = b0 / a0
    b1 = b1 / a0

    w1 = next(source)
    yield b0 * w1

    while True:
        w0 = next(source) - a1 * w1
        yield b0 * w0 + b1 * w1
        w1 = next(source) - a1 * w0
        yield b0 * w1 + b1 * w0


def twopole(source, a0, a1, a2, b0):
    """Two pole filter a0 y[n] = b0 x[n] - a1 y[n-1] - a2 y[n-2]."""
    source = iter(source)
    a1 = a1 / a0
    a2 = a2 / a0
    b0 = b0 / a0

    y1 = b0 * next(source)
    yield y1
    y0 = b0 * next(source) - a1 * y1
    yield y0

    while True:
        y2 = y0
        y0 = b0 * next(source) - a1 * y0 - a2 * y1
        yield y0
        y1 = y0
        y0 = b0 * next(source) - a1 * y0 - a2 * y2
        yield y0


def twozero(source, a0, b0, b1, b2):
    """Two zero filter a0 y[n] = b0 x[n] + b1 x[n-1] + b2 x[n-2]."""
    source = iter(source)
    b0 = b0 / a0
    b1 = b1 / a0
    b2 = b2 / a0

    x1 = next(source)
    yield b0 * x1
    x2 = next(source)
    yield b0 * x2 + b1 * x1

    while True:
        x0 = next(source)
        yield b0 * x0 + b1 * x2 + b2 * x1
        x1 = next(source)
        yield b0 * x1 + b1 * x0 + b2 * x2
        x2 = next(source)
        yield b0 * x2 + b1 * x1 + b2 * x0


def biquad(source, a0, a1, a2, b0, b1, b2):
    """Two pole two zero filter a0 y[n] = b0 x[n] + b1 x[n-1] + b2 x[n-2] - a1 y[n-1] - a2 y[n-2]."""
    source = iter(source)
    a1 = a1 / a0
    a2 = a2 / a0
    b0 = b0 / a0
    b1 = b1 / a0
    b2 = b2 / a0

    w1 = next(source)
    yield b0 * w1
    w0 = next(source) - a1 * w1
    yield b0 * w0 + b1 * w1

    while True:
        w2 = w0
        w0 = next(source) - a1 * w0 - a2 * w1
        yield b0 * w0 + b1 * w2 + b2 * w1
        w1 = w0
        w0 = next(source) - a1 * w0 - a2 * w2
        yield b0 * w0 + b1 * w1 + b2 * w2


def dynamic_biquad(source, coefs):
    """Dynamic two pole two zero filter a0[n] y[n] = b0[n] x[n] + b1[n] x[n-1] + b2[n] x[n-2] - a1[n] y[n-1] - a2[n] y[n-2]."""
    source = iter(source)
    coefs = iter(coefs)
    
    #Dynamic filters do not commute. Direct form 2 is impossible to implement.
    #Think y[n] = b0[n] x[n] + y[n-1] with b0[n] changing from 0 to 1 at some instant n0.
    #w[n] = x[n] + w[n-1]
    #y[n] = b0[n] w[n], would result in y[n0] containing the sum of all samples x[k], k < n0 and not just x[n0] as it should.

    a0, a1, a2, b0, b1, b2 = next(coefs)
    x2 = next(source)
    y1 = (b0 * x2) / a0
    yield y1
    a0, a1, a2, b0, b1, b2 = next(coefs)
    x1 = next(source)
    y0 = (b0 * x1 + b1 * x2 - a1 * y1) / a0
    yield y0

    #By doing six rounds we save one asignment per round. Now ain't that something.
    while True:
        a0, a1, a2, b0, b1, b2 = next(coefs)
        x0 = next(source)
        y2 = y0
        y0 = (b0 * x0 + b1 * x1 + b2 * x2 - a1 * y0 - a2 * y1)/a0
        yield y0

        a0, a1, a2, b0, b1, b2 = next(coefs)
        x2 = next(source)
        y1 = y0
        y0 = (b0 * x2 + b1 * x0 + b2 * x1 - a1 * y0 - a2 * y2)/a0
        yield y0

        a0, a1, a2, b0, b1, b2 = next(coefs)
        x1 = next(source)
        y2 = y0
        y0 = (b0 * x1 + b1 * x2 + b2 * x0 - a1 * y0 - a2 * y1)/a0
        yield y0

        #Now x and y are out of phase, needs three more rounds.

        a0, a1, a2, b0, b1, b2 = next(coefs)
        x0 = next(source)
        y1 = y0
        y0 = (b0 * x0 + b1 * x1 + b2 * x2 - a1 * y0 - a2 * y2)/a0
        yield y0

        a0, a1, a2, b0, b1, b2 = next(coefs)
        x2 = next(source)
        y2 = y0
        y0 = (b0 * x2 + b1 * x0 + b2 * x1 - a1 * y0 - a2 * y1)/a0
        yield y0

        a0, a1, a2, b0, b1, b2 = next(coefs)
        x1 = next(source)
        y1 = y0
        y0 = (b0 * x1 + b1 * x2 + b2 * x0 - a1 * y0 - a2 * y2)/a0
        yield y0
