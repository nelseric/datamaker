import sys
import os.path

import pandas as pd
import numpy as np

import datamaker.util as util

def import_data():
  if not len(sys.argv) > 1:
    print "Please provide input datafile"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input datafile"
    exit(1)

  store = pd.HDFStore(input_file_name + '.h5')

  data_file = pd.read_csv(
    input_file_name,
    compression="gzip",
    engine='c',
    chunksize=200000,
    # iterator=True,
    parse_dates={"time": ["Timestamp"]},
    infer_datetime_format=True,
    warn_bad_lines=True,
    index_col=0
  )

  total = 65138838
  cur = 0

  bid_ask = None
  exit_for_real = False

  for ticks in data_file:
    ask = ticks['Ask price'].resample('1Min', how='ohlc')
    bid = ticks['Bid price'].resample('1Min', how='ohlc')
    ask_vol = ticks['Ask volume'].resample('1Min', how='sum')
    bid_vol = ticks['Bid volume'].resample('1Min', how='sum')

    calculated  = pd.concat([ask, bid, ask_vol, bid_vol], axis=1, keys=['Ask', 'Bid', 'Bid Volume', 'Ask Volume'])

    if(bid_ask.__class__ != None.__class__):
      bid_ask = merge_chunks(bid_ask, calculated)
    else:
      bid_ask = calculated

    print bid_ask.ix[-1].name

  store.put("ticks_ohlcv", bid_ask)


def merge_chunks(old, new):
  new_fixed = new.ix[1:]
  old.ix[-1] = merge_ohlcv(old.ix[-1], new.ix[0])
  return old.append(new_fixed, verify_integrity=True)

def merge_ohlcv(old, new):
  old['Ask']['close'] = new['Ask']['close']
  old['Bid']['close'] = new['Bid']['close']

  if old['Ask']['high'] < new['Ask']['high']:
    old['Ask']['high'] = new['Ask']['high']
  if old['Ask']['low'] > new['Ask']['low']:
    old['Ask']['low'] = new['Ask']['low']

  if old['Bid']['high'] < new['Bid']['high']:
    old['Bid']['high'] = new['Bid']['high']
  if old['Bid']['low'] > new['Bid']['low']:
    old['Bid']['low'] = new['Bid']['low']

  old['Ask Volume'] = old['Ask Volume'] + new['Ask Volume']
  old['Bid Volume'] = old['Bid Volume'] + new['Bid Volume']
  return old
