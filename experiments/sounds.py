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