from pylab import *

from waveform import *

N = 1000

t = linspace(-0.5, 0.7, N)
x = t / pi

tri = vectorize(triangle)

cub = vectorize(cub)
saw_c = vectorize(saw_complement)

#plot(saw(t / 2 / pi))
#plot(tri(t))

def cub_complement_(phase):
    x = phase - floor(phase + 0.5)
    if x < -0.485:
        return -141.683313066 + x * (-890.871247193 + x * (-1877.70991482 - 1315.78489017 * x))
    elif x < -0.45:
        return -14.4841833281 + x * (-107.462486507 + x * (-269.423768994 - 215.237469947 * x))
    elif x < -0.4:
        return -2.72415704125 + x * (-29.4601745573 + x * (-96.9694386506  - 88.148440549 * x))
    elif x < -0.35:
        return -0.242340474369 + x * (-11.0004026851 + x * (-51.2046399185 + -50.3316340626 *x))
    elif x < -0.25:
        return 0.645147736088 + x * (-3.29984031237 + x * (-28.9358315141 - 28.8687673678 * x))
    elif x < -0.15:
        return 0.871037573309 + x * (-0.634232323039 + x * (-18.4536797861 - 15.1329387029 * x))
    elif x < 0.15:
        x2 = x * x
        return 0.90154267737 + x2 * (-13.6879509584 + 16.7397805313 * x2)
    elif x < 0.25:
        return 0.871037573309 + x * (0.634232323039 + x * (-18.4536797861 + 15.1329387029 * x))
    elif x < 0.35:
        return 0.645147736088 + x * (3.29984031237 + x * (-28.9358315141 + 28.8687673678 * x))
    elif x < 0.4:
        return -0.242340474369 + x * (11.0004026851 + x * (-51.2046399185 + 50.3316340626 *x))
    elif x < 0.45:
        return -2.72415704125 + x * (29.4601745573 + x * (-96.9694386506  + 88.148440549 * x))
    elif x < 0.485:
        return -14.4841833281 + x * (107.462486507 + x * (-269.423768994 + 215.237469947 * x))
    else:
        return -141.683313066 + x * (890.871247193 + x * (-1877.70991482 + 1315.78489017 * x))

cub_c_ = vectorize(cub_complement_)

#plot(sum((-1)**k * cos(t * (1 + k)) / (1 + k) for k in range(1000)))
def d_cub_c(t):
    return sum(-(-1)**k * sin(2 * pi * t * (1 + k)) / (1 + k)**2 for k in range(N)) * 2 * pi

def cub_c(t):
    return sum((-1)**k * cos(2 * pi * t * (1 + k)) / (1 + k)**3 for k in range(N))

#print par_c(0.45)

x0 = 0.485
px0 = cub_c(x0)
dpx0 = d_cub_c(x0)
x = 0.5
px = cub_c(x)
dpx = d_cub_c(x)

def Power(x, n):
    return x**n

c = (px0*Power(x,2)*(x - 3*x0) + 
        x0*(dpx0*Power(x,2)*(-x + x0) + 
           x0*(px*(3*x - x0) + dpx*x*(-x + x0))))/Power(x - x0,3)

a = (dpx0*Power(x,3) + x*(-6*px + 6*px0 + (2*dpx + dpx0)*x)*
         x0 - (dpx + 2*dpx0)*x*Power(x0,2) - dpx*Power(x0,3))/Power(x - x0,3)

b = (3*px*(x + x0) - 3*px0*(x + x0) - 
        (x - x0)*(dpx*x + 2*dpx0*x + 2*dpx*x0 + dpx0*x0))/Power(x - x0,3)

d = (-2*px + 2*px0 + (dpx + dpx0)*(x - x0))/Power(x - x0,3)


print c, a, b, d

appr = c + a * t + b * t * t + d * t ** 3

#for mu in 0.65 + arange(100) * 0.01 * 0.05:
#mu = 0.69
#appr = (sqrt(0.5 - t) / sqrt(0.05) * mu + (0.5 - t) / 0.05 * (1 - mu)) * par_c(0.45)
#print mu, e
#print a, b, d
#c = 0.9015426773696957
#a = -(4*c - 4*px + dpx*x)/(2*Power(x,2))
#b = (2*c - 2*px + dpx*x)/(2*Power(x,4))


#print c, a, b

cub_complement = cub_c(t)
plot(t, cub_complement)
plot(t, cub_c_(t))
#appr = c + a * t**2 + b * t**4

plot(t, appr * (x0 < t) * (t < x))

e = max(abs(cub_complement - appr) * (x0 < t) * (t < x))
print e

#plot(t, appr * (t > 0.45))

#plot(t, cub(t))
#plot(t[:-1], diff(cub_complement) / (t[1] - t[0]))
#plot(t, d_cub_c(t))
show()



#x = 0.15
#b = par_c(x)
#c = (b - a * x) / x**3

#print a, c

#plot(t, t * (a + c * t * t))
"""
xs = []
es = []
for x in arange(1, 200) / 200.0 * 0.2:
#x = 1
    b = par_c(x)
    # a * x + c * x ** 3 = b
    # c = (b - a * x) / x**3
    appr = a * t + (b - a * x) / x ** 3 * t ** 3
    #plot(t, appr * (abs(t) < x))
    e = max((par_complement - appr) * (abs(t) < x))
    #print x, e
    #es.append(e)
    #xs.append(x)
"""
#plot(xs, es)


#plot(diff(par_complement) / (t[1] - t[0]))
#plot(2.5 * (x - x*x*x))

# Impulse train Hilbert transform
#plot(1.0 / tan(t * 0.5))
# Integral
#plot(log(sin(t * 0.5)))
# Double Integral


#show()
