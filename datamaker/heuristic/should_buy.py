import numpy as np

from datamaker.feature import Feature
import pandas as pd

import IPython


class ShouldBuy(Feature):

    """
        This calculates whether or not the pair price will hit the upper limit
        before it hits the lower limit, or the search limit.

        This basically checks if a purchase limit order placed at
        a specific time will be successful.

        :param data: OHLCV Currency pair data
        :param take_profit: The high value offset for a limit order
        :param stop_loss: The low value offset for a limit order
        :param search_limit: Limits the search range of the limit
                             orders, to speed computation

        Without the search limit, this calculation is O(n^2) worst case, when
        it is used, this is calculated in O(n)
    """

    def __init__(self, take_profit, stop_loss, search_limit=14400):
        
        super(ShouldBuy, self).__init__()
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.search_limit = search_limit

    def __repr__(self):
        return "ShouldBuy(tp={},sl={},sl={})".format(self.take_profit, self.stop_loss, self.search_limit)

    def _calculate(self, data):
        result = pd.DataFrame(
            apply(data, self.take_profit,
                  self.stop_loss, self.search_limit),
            index=data.index
        )
        result.columns = ["ShouldBuy"]
        return result


def apply(df, margin_upper, margin_lower, limit):

    target_high = df["closeAsk"] + margin_upper
    target_low = df["closeAsk"] - margin_lower

    df2 = pd.concat([df["highBid"], df["lowBid"], target_high, target_low], axis=1)

    data = df2.values

    n = len(data)
    res = np.empty(n)

    bid_high = 0
    bid_low = 1
    target_high_i = 2
    target_low_i = 3  

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
