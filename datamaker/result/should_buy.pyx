cimport cython
cimport numpy as npc

import numpy as np

from datamaker.feature import Feature

# 0 Ask         open            1.084150
# 1             high            1.084150
# 2             low             1.083600
# 3             close           1.083900
# 4 Bid         open            1.084000
# 5             high            1.084000
# 6             low             1.083250
# 7             close           1.083350
# 8 Bid Volume  Ask volume     70.700001
# 9 Ask Volume  Bid volume    124.599999

class ShouldBuy(Feature):

  """should_buy result value"""
  def __init__(self, data, margin_upper = 0.00055, margin_lower = 0.00015, search_limit = 1440):
    super(ShouldBuy, self).__init__(data)
    self.margin_upper = margin_upper
    self.margin_lower = margin_lower
    self.search_limit = search_limit

  def calculate(self):
    self._result = apply(self.data.values, self.margin_upper, self.margin_lower, self.search_limit)

cpdef npc.ndarray apply(npc.ndarray[double, ndim=2] data, double margin_upper, double margin_lower, int limit):

  cdef Py_ssize_t i, cmp_limit, n = len(data)
  cdef npc.ndarray res = np.empty(n)

  cdef double target_high, target_low

  for i in range(n):
    if i + limit > n:
      cmp_limit = n - i
    else:
      cmp_limit = limit

    target_high = data[i][3] + margin_upper
    target_low = data[i][3] - margin_lower

    res[i] = False
    for j in range(cmp_limit):
      if data[j][5] >= target_high:
        res[i] = True
        break
      elif data[j][6] <= target_low:
        break
  return res
