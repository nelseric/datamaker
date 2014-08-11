import sys
import os.path

import pandas as pd
import numpy as np

import datamaker.util as util

import IPython

from functools import partial


def do_input_stuff():
  if not len(sys.argv) > 1:
    print "Please provide input database"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input database"
    exit(1)

  store = pd.HDFStore(input_file_name)

  print "Loading 'ticks_ohlcv'"
  data = store.get('ticks_ohlcv')

  p_should_buy = partial(should_buy, data, margin_high = 0.00055)

  print "Applying should_buy"
  data["should_buy"] = data.apply(p_should_buy, axis=1)

  IPython.embed()
  store.close()



def should_buy(dataset, row, margin_high, margin_low = None, time_limit = 360):
  margin_low = margin_low or margin_high

  target_high = row['Ask']['close'] + margin_high
  target_low = row['Ask']['close'] - margin_low

  index = dataset.index.get_loc(row.name)

  if index % 1000 == 0:
    print row.name

  for i in range(time_limit):
    cmp_row = dataset.ix[index + i + 1]
    if cmp_row['Bid']['high'] >= target_high:
      return True
    elif cmp_row['Bid']['low'] <= target_low:
      return False
  return False
