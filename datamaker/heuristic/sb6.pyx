## cython: profile=True,linetrace=True,binding=True

cimport cython

import numpy as np
cimport numpy as np

import pandas as pd

def apply(df, margin_upper, margin_lower, limit):

    target_high = df["closeAsk"] + margin_upper
    target_low = df["closeAsk"] - margin_lower

    df2 = pd.concat([df["highBid"], df["lowBid"], target_high, target_low], axis=1)
    capply(df2.values, margin_upper, margin_lower, limit)

@cython.boundscheck(False)
cdef np.ndarray[np.int_t, ndim=1] capply(np.ndarray[double, ndim=2] data,
                        double margin_upper, double margin_lower,
                        int limit):
    print("in apply")
    cdef Py_ssize_t i, cmp_limit, n = len(data)
    cdef np.ndarray[np.int_t, ndim=1] res = np.empty(n, dtype=np.int)
    
    cdef double target_high, target_low

    cdef int bid_high = 0
    cdef int bid_low = 1
    cdef int target_high_i = 2
    cdef int target_low_i = 3

    for i in range(n):
        if i % 1440 == 0:
            print "{0:0.4f}".format((float(i)/n) * 100.0)

        if i + limit > n:
            cmp_limit = n - i
        else:
            cmp_limit = limit

        target_high = data[i][target_high_i]
        target_low = data[i][target_low_i]

        res[i] = 0
        for j in range(cmp_limit):
            if data[i + j][bid_high] >= target_high:
                res[i] = 1
                break
            elif data[i + j][bid_low] <= target_low:
                res[i] = 0
                break
    return res
