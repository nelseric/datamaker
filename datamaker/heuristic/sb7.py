## cython: profile=True,linetrace=True,binding=True

# cimport cython

import numpy as np
# cimport numpy as np

import pandas as pd

def apply(df, margin_upper, margin_lower, limit):

    target_high = df["closeAsk"] + margin_upper
    target_low = df["closeAsk"] - margin_lower

    df2 = pd.concat([df["highBid"], df["lowBid"], target_high, target_low], axis=1)

    data = df2.values

    n = len(data)
    res = np.empty(n)

    bid_high = 0
    bid_low = 1
    target_high = 2
    target_low = 3  

    for i in range(n):
        if i % 1440 == 0:
            print "{0:0.4f}".format((float(i)/n) * 100.0)

        if i + limit > n:
            cmp_limit = n - i
        else:
            cmp_limit = limit

        target_high = data[i][target_high]
        target_low = data[i][target_low]

        res[i] = 0
        for j in range(cmp_limit):
            if data[i + j][bid_high] >= target_high:
                res[i] = 1
                break
            elif data[i + j][bid_low] <= target_low:
                res[i] = 0
                break
    return res
