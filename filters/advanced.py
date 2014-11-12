from base import *
from filters.base import *
from filters.basic import *
from filters.delay import *


def reverb(source):
    g = 0.45
    d = 0.6
    lpf_ = lambda s: onepole(s, 1, -d, g * (1 - d))

    def lbcf(source, duration):
        return filtered_comb_t(source, 0.05, lpf_)

    s0, s1, s2 = tee(source, 3)
    return gain_gen(schroeder_t(schroeder_t(mix_gen([lbcf(s0, 0.035), lbcf(s1, 0.011), lbcf(s2, 0.027)]), 0.0057, 0.5), 0.0091, 0.5), 0.3)
