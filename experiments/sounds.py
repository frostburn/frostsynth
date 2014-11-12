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