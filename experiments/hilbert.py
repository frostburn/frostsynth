from pylab import *

from osc import *

N = 5000

t = linspace(-0.5, 0.5, N)
x = t / pi

tri = vectorize(triangle)

saw = vectorize(saw)
saw_c = vectorize(saw_complement)

#plot(saw(t / 2 / pi))
#plot(tri(t))

def par_complement_(phase):
    x = phase - floor(phase + 0.5)
    if x < -0.45:
        xx = (0.5 + x)
        return xx * (-6.50377029198 + 39.1640305629 * xx) - 0.82780791828 * sqrt(xx)
    elif x < -0.4:
        return -6.52202646969 + x * (-47.7235413275 + x * (-131.454491059 - 123.496136031 * x))
    elif x < -0.35:
        return -1.22922321362 + x * (-8.5259921333 + x * (-34.7068061396 - 43.9115553199 * x))
    elif x < -0.25:
        return -0.167319598632 + x * (0.61647503263 + x * (-8.46993943614 - 18.8140327989 * x))
    elif x < -0.15:
        return -0.0107270508022 + x * (2.43730170152 + x * (-1.4197683794 - 9.72465221494 * x))
    elif x < 0.15:
        return x * (2.64762720183 - 6.4289442721 * x * x)
    elif x < 0.25:
        return 0.0107270508022 + x * (2.43730170152 + x * (1.4197683794 - 9.72465221494 * x))
    elif x < 0.35:
        return 0.167319598632 + x * (0.61647503263 + x * (8.46993943614 - 18.8140327989 * x))
    elif x < 0.4:
        return 1.22922321362 + x * (-8.5259921333 + x * (34.7068061396 - 43.9115553199 * x))
    elif x < 0.45:
        return 6.52202646969 + x * (-47.7235413275 + x * (131.454491059 - 123.496136031 * x))
    else:
        xx = (0.5 - x)
        return xx * (6.50377029198 - 39.1640305629 * xx) + 0.82780791828 * sqrt(xx)

par_c_ = vectorize(par_complement_)

#plot(sum((-1)**k * cos(t * (1 + k)) / (1 + k) for k in range(1000)))
def d_par_c(t):
    return (log(1 + cos(2 * pi * t)) + log(2)) * 6 / pi

def par_c(t):
    return 6 / pi / pi * sum((-1)**k * sin(2 * pi * t * (1 + k)) / (1 + k)**2 for k in range(N))

print par_c(0.45)

x0 = 0.45
px0 = par_c(x0)
dpx0 = d_par_c(x0)
x = 0.49
px = par_c(x)
dpx = d_par_c(x)

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

par_complement = par_c(t)
plot(t, par_complement)
#appr = c + a * t + b * t * t + d * t ** 3
#plot(t, appr * (x0 < t) * (t < x))

#for mu in 0.65 + arange(100) * 0.01 * 0.05:
#mu = 0.69
#appr = (sqrt(0.5 - t) / sqrt(0.05) * mu + (0.5 - t) / 0.05 * (1 - mu)) * par_c(0.45)
#print mu, e

tt = (0.5 - t)
p = par_c(0.45)
dp = d_par_c(0.45)
p2 = par_c(0.5 - 0.01)
a = -5.567223249782442*dp + 314.0333949869465*p - 365.3778599825953*p2
b = 50.44815499854961*dp - 2226.8892999129766*p + 2435.8523998839682*p2
d = 0.6808414436620696*dp - 40.85048661972417*p + 54.467315492965554*p2
a = 2.4352899911183377*dp + 104.58804960032518*p - 179.41124888979215*p2
b = -29.568599940788914*dp - 830.5869973355011*p + 1196.0749925986142*p2
d = -0.21396039917104484*dp - 9.628217962697017*p + 26.7450498963806*p2
appr = a * tt + b * tt * tt + d * sqrt(tt)

print a, b, d

e = max(abs(par_complement - appr) * (x0 < t) * (t < x))
print e

#plot(t, appr * (t > 0.45))

plot(t, par_c_(t))
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
