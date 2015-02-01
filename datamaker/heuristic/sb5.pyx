cimport cython

import numpy as np
cimport numpy as np

from datamaker.feature import Feature

def apply(df, high, low, limit):
    capply(df, high, low, limit)

@cython.boundscheck(False)
cdef np.ndarray[np.int_t, ndim=1] capply(np.ndarray[double, ndim=2] data,
                        double margin_upper, double margin_lower,
                        int limit):
    print("in apply")
    cdef Py_ssize_t i, cmp_limit, n = len(data)
    cdef np.ndarray[np.int_t, ndim=1] res = np.empty(n, dtype=np.int)

    cdef double target_high, target_low

    cdef int ask_close = 0
    cdef int bid_high = 3
    cdef int bid_low = 5

    for i in range(n):
        if i % 1440 == 0:
            print "{0:0.4f}".format((float(i)/n) * 100.0)

        if i + limit > n:
            cmp_limit = n - i
        else:
            cmp_limit = limit

        target_high = data[i][ask_close] + margin_upper
        target_low = data[i][ask_close] - margin_lower

        res[i] = 0
        for j in range(cmp_limit):
            if data[i + j][bid_high] >= target_high:
                res[i] = 1
                break
            elif data[i + j][bid_low] <= target_low:
                res[i] = 0
                break
    return res
