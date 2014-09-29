import sys
import os.path

import pandas as pd
import numpy as np

import IPython

def import_data():
  if not len(sys.argv) > 1:
    print "Please provide input datafile"
    exit(1)

  input_file_name = sys.argv[1]

  if not os.path.isfile(input_file_name):
    print "Please provide input datafile"
    exit(1)

  store = pd.HDFStore(os.path.join('data/', os.path.basename(input_file_name).split('.')[0] + '.h5'))

  comp_ext = {
    "bz2": "bz2",
    "gz": "gzip",
    "csv": None
  }
  comp = comp_ext[input_file_name.split('.')[-1]]


  data_file = pd.read_csv(
    input_file_name,
    compression=comp,
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

  data = None

  for ticks in data_file:
    ask = ticks['Ask price'].resample('1Min', how='ohlc')
    bid = ticks['Bid price'].resample('1Min', how='ohlc')
    ask['volume'] = ticks['Ask volume'].resample('1Min', how='sum')
    bid['volume'] = ticks['Bid volume'].resample('1Min', how='sum')

    calculated  = pd.concat([ask, bid], axis=1, keys=['Ask', 'Bid'])

    if(data.__class__ != None.__class__):
      data = merge_chunks(data, calculated)
    else:
      data = calculated

    print data.ix[-1].name

  data.columns = ['_'.join(col).strip() for col in data.columns.values]

  store.put("ticks_ohlcv", data)


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

  old['Ask']['volume'] = old['Ask']['volume'] + new['Ask']['volume']
  old['Bid']['volume'] = old['Bid']['volume'] + new['Bid']['volume']
  return old
