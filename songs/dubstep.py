# Intro
beat = 0.1
pitch = eased_step_gen(cycle([(C3, 3 * beat, 0.02), (D3, beat), (G3, 2 * beat), (A3, 2 * beat)]))
transpose = eased_step_gen(cycle([(unison, beat * 32, 0.02), (fifth, beat * 32)]))
f = map(mtof, add_gen(pitch, transpose))
p = integrate_gen(f)
s = (0.25 * softsquare(p, 1 - exp(-t * 0.5)) for t, p in zip(time_gen(), p))

s = Infinitee(chain(timeslice(s, 128 * beat), zero_t(3)))

s = list(comb_t(s, 2 * beat, 0.5))



# Base fade-in
#w = irfft_waveform([cunit() * i ** -0.5 / 50.0 for i in range(200) if i > 0])
#w1 = irfft_waveform([cunit() * i ** -0.5 / 50.0 for i in range(200) if i > 0])

w = WaveForm(irfft([b * abs(b) ** -0.6 * i ** -1 if i > 0 else 0.0 for i, b in enumerate(rfft((uniform(256))))]))
#w = WaveForm(uniform(128))

f = [75 + t for t in time(10)]

s = [w(t * f + sine(t * f * 0.51) * t) for t, f in zip(time_gen(), f)]

s = gain(dynamic_lowpass(s, (200 + t * 100 * softrect(t + cub(t * 2) * 0.1, 0.8, 0.8) for t in time_gen()), 1), 10.0)

s = mix([s, lpf(s, 300)], [1, 0.4])