from cffi import FFI


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
