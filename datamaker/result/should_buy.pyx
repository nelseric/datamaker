cimport cython
cimport numpy as npc

import numpy as np

from datamaker.feature import Feature
import pandas as pd

class ShouldBuy(Feature):

  """
    This calculates whether or not the pair price will hit the upper limit before
    it hits the lower limit, or the search limit.

    This basically checks if a purchase limit order placed at a specific time will be successful.

    :param data: OHLCV Currency pair data
    :param limit_upper: The high value offset for a limit order
    :param limit_lower: The low value offset for a limit order
    :param search_limit: Limits the search range of the limit orders, to speed computation

    Without the search limit, this calculation is O(n^2) worst case, when it is used, this is calculated in O(n)
  """
  def __init__(self, limit_upper = 0.00055, limit_lower = 0.00015, search_limit = 1440, *args, **kwargs):
    super(ShouldBuy, self).__init__(*args, **kwargs)
    self.limit_upper = limit_upper
    self.limit_lower = limit_lower
    self.search_limit = search_limit

  def _calculate(self, data):
    result = pd.DataFrame(
      apply(data.values, self.limit_upper, self.limit_lower, self.search_limit),
      index=data.index
    )
    result.columns = ["ShouldBuy"]
    return result


cpdef npc.ndarray apply(npc.ndarray[double, ndim=2] data, double margin_upper, double margin_lower, int limit):
  # """
  #   This does the actual computation for ShouldBuy. It expects the data at the following indexes:
  #     0 Ask         open            1.084150 Ask_close
  #     1             high            1.084150 Bid_close
  #     2             low             1.083600 Ask_high
  #     3             close           1.083900 Bid_high
  #     4 Bid         open            1.084000 Ask_low
  #     5             high            1.084000 Bid_low
  #     6             low             1.083250 Ask_open
  #     7             close           1.083350 Bid_open
  #     8 Bid Volume  Ask volume     70.700001 volume
  #     9 Ask Volume  Bid volume    124.599999
  # """
  cdef Py_ssize_t i, cmp_limit, n = len(data)
  cdef npc.ndarray res = np.empty(n)

  cdef double target_high, target_low
  
  ask_close = 0
  bid_high = 3
  bid_low = 5
  
  for i in range(n):
    if i + limit > n:
      cmp_limit = n - i
    else:
      cmp_limit = limit

    target_high = data[i][ask_close] + margin_upper
    target_low = data[i][ask_close] - margin_lower

    res[i] = False
    for j in range(cmp_limit):
      if data[j][bid_high] >= target_high:
        res[i] = True
        break
      elif data[j][bid_low] <= target_low:
        break
  return res
