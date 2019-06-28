import numpy as np
cimport numpy as np

install_command = r"python setup.py build_ext --inplace"

def calculate_scatters(np.ndarray[np.double_t, ndim=1] K1, np.ndarray[np.double_t, ndim=2] K2, int n):
    cdef np.ndarray scatters = np.zeros([n, n], np.double)
    cdef int i, j
    for i in range(n):
        for j in range(i, n):
            scatters[i, j] = K1[j+1] - K1[i] - \
                            (K2[j+1, j+1] + K2[i, i] - K2[j+1, i] - K2[i, j+1]) / (j - i + 1);
            
    return scatters

def calculate_change_points(int m, int n, 
                            np.ndarray[np.double_t, ndim=2] I, 
                            np.ndarray[np.double_t, ndim=2] J, 
                            int lmin, int lmax, 
                            np.ndarray[np.int64_t, ndim=2] p,
                            bint backtrack):
    cdef double c
    cdef int k, l, t

    for k in range(1, m+1):
        for l in range((k+1)*lmin, n+1):
            I[k, l] = 1e100
            for t in range(max(k*lmin, l-lmax), l-lmin+1):
                c = I[k-1, t] + J[t, l-1]
                if c < I[k, l]:
                    I[k, l] = c
                    if backtrack:
                        p[k, l] = t

    return p
