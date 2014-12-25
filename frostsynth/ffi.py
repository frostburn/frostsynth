from math import pi, floor
from cffi import FFI

from frostsynth import two_pi, i_two_pi

__all__ = ["fft"]


ffi = FFI()


ffi.cdef(
    """
    double lcg();
    void lcg_a(double *a, size_t l);
    void fft_r(double *a, size_t l);
    void convolve(const double Signal[/* SignalLen */], size_t SignalLen,
                  const double Kernel[/* KernelLen */], size_t KernelLen,
                  double Result[/* SignalLen + KernelLen - 1 */]);
    void malloc_copy(double result[], size_t length, size_t count);
    double precycloid_m1(double x, double a);
    double precycloid(double x, double a);

    double j0(double x);
    double j1(double x);
    double jn(int n, double x);
    double y0(double x);
    double y1(double x);
    double yn(int n, double x);
    """
)


C = ffi.verify(
    """
    #include <stdlib.h>
    #include <complex.h>
    #include <math.h>

    unsigned int x;

    double lcg()
    {
        x = 1664525 * x + 1013904223;
        return x / 2147483648.0 - 1.0;
    }

    void lcg_a(double *a, size_t l)
    {
        size_t i;
        for (i = 0; i < l; i++){
            x = 1664525 * x + 1013904223;
            a[i] = x / 2147483648.0 - 1.0;
        }
    }

    double complex twiddles[32] = {1,
     (0.99518472667219693-0.098017140329560604*I),
     (0.98078528040323043-0.19509032201612825*I),
     (0.95694033573220882-0.29028467725446233*I),
     (0.92387953251128674-0.38268343236508978*I),
     (0.88192126434835505-0.47139673682599764*I),
     (0.83146961230254524-0.55557023301960218*I),
     (0.77301045336273699-0.63439328416364549*I),
     (0.70710678118654757-0.70710678118654746*I),
     (0.63439328416364549-0.77301045336273699*I),
     (0.55557023301960229-0.83146961230254524*I),
     (0.47139673682599781-0.88192126434835494*I),
     (0.38268343236508984-0.92387953251128674*I),
     (0.29028467725446233-0.95694033573220894*I),
     (0.19509032201612833-0.98078528040323043*I),
     (0.09801714032956077-0.99518472667219682*I),
     -I,
     (-0.098017140329560645-0.99518472667219693*I),
     (-0.19509032201612819-0.98078528040323043*I),
     (-0.29028467725446216-0.95694033573220894*I),
     (-0.38268343236508973-0.92387953251128674*I),
     (-0.4713967368259977-0.88192126434835505*I),
     (-0.55557023301960196-0.83146961230254546*I),
     (-0.63439328416364538-0.7730104533627371*I),
     (-0.70710678118654746-0.70710678118654757*I),
     (-0.77301045336273699-0.63439328416364549*I),
     (-0.83146961230254535-0.55557023301960218*I),
     (-0.88192126434835494-0.47139673682599786*I),
     (-0.92387953251128674-0.38268343236508989*I),
     (-0.95694033573220882-0.29028467725446239*I),
     (-0.98078528040323043-0.19509032201612861*I),
     (-0.99518472667219682-0.098017140329560826*I)};

    void fft(double complex *a, size_t l)
    {
        if (l == 2){
            double complex a0 = a[0];
            a[0] += a[1];
            a[1] = a0 - a[1];
        }
        else if (l == 4){
            double complex a0 = a[0];
            double complex a1 = a[1];
            double complex a2 = a[2];
            double complex a3 = a[3];
            double complex t0 = I * (a1 - a3);
            double complex t1 = a0 - a2;
            a[0] += a1 + a2 + a3;
            a[1] = t1 - t0;
            a[2] += a0 - a1 - a3;
            a[3] = t1 + t0;
        }
        else if (l >= 4){
            size_t i;
            size_t l2 = l >> 1;
            double i_l = 1.0 / l;
            double complex twiddle;

            double complex *even = (double complex *) malloc(l2 * sizeof(double complex));
            double complex *odd = (double complex *) malloc(l2 * sizeof(double complex));
            for(i = 0; i < l2; i++){
                even[i] = a[2 * i];
                odd[i] = a[2 * i + 1];
            }
            fft(even, l2);
            fft(odd, l2);
            for (i = 0; i < l2; i++){
                if (l == 8){
                    twiddle = twiddles[i << 3];
                }
                else if (l == 16){
                    twiddle = twiddles[i << 2];
                }
                else if (l == 32){
                    twiddle = twiddles[i << 1];
                }
                else if (l <= 64){
                    twiddle = twiddles[i];
                }
                else{
                    twiddle = cexp(-I * 2 * M_PI * i * i_l);
                }
                a[i] = even[i] + twiddle * odd[i];
                a[i + l2] = even[i] - twiddle * odd[i];
            }
            free(even);
            free(odd);
        }
    }


    void fft_r(double *a, size_t l){
        size_t i;
        double complex *b = malloc(l * sizeof(double complex));
        for (i = 0; i < l; i++){
            b[i] = a[2 * i] + a[2 * i + 1] * I;
        }
        fft(b, l);
        for (i = 0; i < l; i++){
            a[2 * i] = creal(b[i]);
            a[2 * i + 1] = cimag(b[i]);
        }
        free(b);
    }

    // Implementation by Alexey Frunze on Stackoverflow.
    void convolve(const double Signal[/* SignalLen */], size_t SignalLen,
                  const double Kernel[/* KernelLen */], size_t KernelLen,
                  double Result[/* SignalLen + KernelLen - 1 */])
    {
      size_t n;

      for (n = 0; n < SignalLen + KernelLen - 1; n++)
      {
        size_t kmin, kmax, k;

        //Result[n] = 0;

        kmin = (n >= KernelLen - 1) ? n - (KernelLen - 1) : 0;
        kmax = (n < SignalLen - 1) ? n : SignalLen - 1;

        for (k = kmin; k <= kmax; k++)
        {
          Result[n] += Signal[k] * Kernel[n - k];
        }
      }
    }

    void malloc_copy(double result[], size_t length, size_t count)
    {
        size_t i, j;
        unsigned char **r = (unsigned char **) malloc(count * sizeof(unsigned char *));
        for (j = 0; j < count; j++){
            r[j] = (unsigned char*) malloc(length * sizeof(unsigned char));
            for (i = 0; i < length; i++){
                result[j * length + i] = r[j][i] / 255.0 * 2.0 - 1.0;
            }
        }
        for (j = 0; j < count; j++){
            free(r[j]);
        }
        free(r);
    }

    #define epsilon (1e-12)
    #define PRECYCLOID_MAX_ITERATIONS (5)

    double precycloid_m1(double x, double a)
    {
        if (x == 0.0){
            return 0.0;
        }
        int i;
        double old_t;
        double t = 1.8171205928321397 * pow(x, 0.3333333333333333) + 0.1 * x;
        for (i = 0; i < PRECYCLOID_MAX_ITERATIONS; i++){
            old_t = t;
            t -= (t + a * sin(t) - x) / (1 + a * cos(t));
            if (fabs(t - old_t) < epsilon){
                break;
            }
        }
        return t;
    }

    double precycloid(double x, double a)
    {
        int i;
        double old_t, t;
        if (x < 3.1){
            double i_a1 = 1.0 / (1.0 + a);
            double x_i_a1 = x * i_a1;
            double y = x_i_a1 * x_i_a1 * i_a1;
            t = x_i_a1 * (1 + y * (a * 0.16666666666666666 + y * (a * (a * 9 - 1) * 0.008333333333333333 + y * (a * (1 - a * (54 - a * 225))) * 0.0001984126984126984)));
        }
        else {
            t = x;
        }
        for (i = 0; i < PRECYCLOID_MAX_ITERATIONS; i++){
            old_t = t;
            t -= (t + a * sin(t) - x) / (1 + a * cos(t));
            if (fabs(t - old_t) < epsilon){
                break;
            }
        }
        return t;
    }
    """,
    libraries=["m"]
)


def uniform(k=None):
    if k is None:
        return C.lcg()
    a = ffi.new("double[]", k)
    C.lcg_a(a, k)
    return list(a)


def _split(x):
    a = ffi.new("double[]", 2 * len(x))
    for i, z in enumerate(x):
        a[2 * i] = z.real
        a[2 * i + 1] = z.imag
    return a


def _recombine(a, N):
    x = [0.0j] * N
    for i in range(N):
        x[i] = complex(a[2 * i], a[2 * i + 1])
    return x


def fft(x):
    N = len(x)
    if N <= 1:
        return x
    if N & (N - 1) != 0:
        raise ValueError("Only power of two lengths supported.")
    a = _split(x)
    C.fft_r(a, N)
    return _recombine(a, N)


def convolve(signal, kernel):
    s = ffi.new("double[]", signal)
    k = ffi.new("double[]", kernel)
    r = ffi.new("double[]", len(signal) + len(kernel) - 1)
    C.convolve(s, len(signal), k, len(kernel), r)
    return list(r)


def malloc_copy(length, count):
    result = ffi.new("double[]", length * count)
    C.malloc_copy(result, length, count)
    return list(result)


def precycloid(x, a=-1.0):
    """Returns t such that x = t + a * sin(t)"""
    if x < 0 or x > two_pi:
        return floor(x * i_two_pi) * two_pi + precycloid(x % two_pi, a)
    elif x > pi:
        return two_pi - precycloid(two_pi - x, a)
    elif a < -0.9 and x < 0.1:
        return C.precycloid_m1(x, a)
    elif a > 0.9 and x > 3.04:
        return pi - C.precycloid_m1(pi - x, -a)
    elif a < 0:
        return pi - C.precycloid(pi - x, -a)
    else:
        return C.precycloid(x, a)


j0 = C.j0;
j1 = C.j1;
jn = C.jn;
y0 = C.y0;
y1 = C.y1;
yn = C.yn;
