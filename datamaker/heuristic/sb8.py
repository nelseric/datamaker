# cython: profile=True,linetrace=True,binding=True

# cimport cython

import numpy as np
# cimport numpy as np
import IPython

import pandas as pd


def apply(df, margin_upper, margin_lower, limit):

    target_high = df["closeAsk"] + margin_upper
    target_low = df["closeAsk"] - margin_lower

    data = pd.concat([df["highBid"], df["lowBid"], target_high, target_low],
                     axis=1, keys=["high", "low", "target_high", "target_low"])
    res = pd.DataFrame(index=data.index)

    bid_high = 0
    bid_low = 1
    target_high = 2
    target_low = 3


    # for i in range(n):
    for i, candle in data.reset_index().iterrows():

        if i % 1440 == 0:
            print "{0:0.4f}".format((float(i) / len(data)) * 100.0)

        if i + limit > len(data):
            cmp_limit = len(data) - i
        else:
            cmp_limit = limit

        res[candle["index"]] = 0
        for j in range(cmp_limit):
            # IPython.embed()
            if data.ix[i + j]["high"] >= candle["target_high"]:
                res[candle["index"]] = 1
                break
            elif data.ix[i + j]["low"] <= candle["target_low"]:
                res[candle["index"]] = 0
                break
    return res
