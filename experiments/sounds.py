# Chaotic rubbery phase locking
def si(source):
    t = 0
    dt = 1.0 / get_srate()
    p = 0
    dp = 220.0 * dt
    for s in source:
        yield cub(p)
        p += dp * (1 + 1.1 * cub(t * 220 - t * t) * s) * 2
        t += dt

s = list(filtered_comb(zero_t(20), 30, si))


# Wood block idea
dt = 1.0 / get_srate()

s = [exp(-2000000 * (t - 0.01) ** 2) for t in time(0.02)] + zero(3)

def signal():
    for i in range(len(s)):
        t = i * dt
        yield s[i - 500] * 0.6 - (s[i - 365] * 0.4 + s[i - 170] * 0.4) * exp(-2 * t)
d = lpf(dc_block(signal()), 1000)

for i in range(len(s)):
    s[i] = s[i] + next(d)

# Cheap cymbal
def train_g():
    noise = uniform_t(3)
    train = fft_train(noise, include_time=True)
    for t, window in train:
        result = []
        for f, n in freq_enumerate(window):
            x = f / 20000.0
            result.append(n * (0.25 + sin(71 * x + 3 * cos(27 * x)) ** 4) * x * exp(-8 * x) * random() ** 2 * exp(-5 * t * (0.5 * x + 1)))
        yield result

s = ifft_train(train_g())

s = gain(s, 20.0)

# Cool FM bass
f = 50

s = [0.5 * sine(f * 4.1 * t + cosine(f * t) * exp(-5 * t)) * exp(-6 * t) for t in time(2)]

# FM Bell
f = 880

s = [0.5 * pen(f * t + cub(0.5 * 7 * f * t) * exp(-3 * t)) * exp(-4 * t) for t in time(2)]

# Nice organ
freq = 220

w = []
for f in freq_window(1 << 16):
    s = 0.0
    for e in range(16):
        p = exp(-0.02 * (f - freq * 2 ** e) ** 2)
        p += exp(-0.02 * (f - freq * 3 ** e) ** 2) * 0.8 / (e + 1)
        p += exp(-0.02 * (f - freq * 5 ** e) ** 2) * 0.4 / (e + 1)
        if e > 3:
            p /= (e - 3) ** 2
        s += p
    s += exp(-0.02 * (f - 6 * freq) ** 2) * 0.5
    s += exp(-0.02 * (f - 10 * freq) ** 2) * 0.2
    w.append(cunit() * s * 5)


s = pseudo_norm_irfft(w)

s = list(resampler3_gen(s, (1.0 + 0.01 * sine(5 * t) for t in time_gen())))

# Adding resonance to an exitation
buf = [0.0] * 200
buf1 = [0.0] * 205
s = []
for j in range(int(2 * srate)):
    t = j / srate
    i = j % len(buf)
    i1 = j % len(buf1)
    e = 0.05 * par(j / len(buf)) * exp(-3 * t) * sine(2 * t)
    y0 = buf[i] * 0.99 + e
    y0_1 = buf1[i1] * 0.97 + e
    buf[i] = y0
    buf1[i1] = y0_1
    s.append(y0 + y0_1)

# Variation of the previous
freq = 100

buf = [0.0] * int(srate / (2.05 * freq))
buf1 = [0.0] * int(srate / (3.05 * freq))
s = []
y0 = 0.0
y0_1 = 0.0
for j in range(int(1 * srate)):
    t = j / srate
    i = j % len(buf)
    i1 = j % len(buf1)
    e0 = duplex(par, freq * j / srate, 0.55) * exp(-1 * t)
    e = e0 * sine(3 * t)
    y0 = y0 * 0.2 + buf[i] * 0.77 + e * 0.05
    y0_1 = y0_1 * 0.2 + buf1[i1] * 0.77 + e * 0.06
    buf[i] = y0
    buf1[i1] = y0_1
    temp = y0 * e + 2 * y0_1 + 0.05 * e + 0.2 * e0
    s.append(0.5 * temp)

# 16bit Bytebeat generator
s = []
for t in range(60 * int(srate)):
    r = (
        t * (17 & (t // 3 ** 8) ^ (t // 3 ** 12)) * 40 & (1 << 15 | 1 << 14) + t * (29 & (t // 3 ** 9) ^ t >> 17) * 20 & (1 << 15 - 1)
    ) & 65535
    s.append(r / (1 << 15) - 1)

# Rhythmic squeaks
s = [0.5 * tanh((cis(105 * t) * constant_series(cis(2500 * t + cis(2 * t)) * (0.7 + 0.25 * sine(3 * t)))).imag * par(0.7 * t)) for t in time(2)]
# Pattern
s = [0.5 * tanh((cis(105 * t) * constant_series(cis(2500 * t - t* t * 100 + cis(2 * t)) * (0.7 + 0.25 * sine(3 * t)))).imag * par(0.7 * t)) for t in time(20)]

# Large bell
s = []
buf = [0.0] * 400
y0 = 0.0
x0 = 0.0
y0_1 = 0.0
x0_1 = 0.0
for k in range_t(3):
    g = -0.99
    i = k % len(buf)
    x1 = x0
    x0 = buf[i] + 0.5 * exp(-0.001 * (k - 1000) ** 2)
    y0 = -g * y0 + g * x0 + x1
    x1_1 = x0_1
    x0_1 = y0
    y0_1 = -g * y0_1 + g * x0_1 + x1_1
    buf[i] = y0_1 * 0.9 - y0 * 0.09
    s.append(y0)

# Wub base
track = [(A2, 0.5, 0.1), C3, Ds3, Es3, E3]
phase = integrate_gen(map(mtof, eased_step_gen(cycle(track))))
phase = gain_gen(phase, 0.5)

s = [saw(p) + saw(p * 1.01 + 0.33) - saw(p * 0.994 + 0.65) + saw(p * 1.022 + 0.76) for p in timeslice(phase, 10)]

train = fft_train(s, include_time=True)

def train_g():
    for t, w in train:
        yield [2 * b * (0.2 + exp(-0.0001 * (f - t * 100 - 50)**2) + exp(-0.0001 * (f - t * 100 - 200)**2)) * exp(-0.0001 * f / (1.01 + softsquare(2 * t, 0.9))) for f, b in freq_enumerate(w)]

s = ifft_train(train_g())
s = gain(s, 0.1)