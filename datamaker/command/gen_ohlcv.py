"""
@author: Eric Nelson
"""

import pandas as pd
import argparse
import dotenv


def gen_ohlcv():
  """
  Take Dukascopy tick data and generate OHLCV data for the pair
  """
  dotenv.load_dotenv('.env')
  parser = argparse.ArgumentParser(description='Run an experiment')
  parser.add_argument('input_file', type=argparse.FileType('r'),
                      help='Tick data file')

  parser.add_argument('output_file', type=argparse.FileType('w'),
                      help='Output OHLCV HDF5 Store')

  args = parser.parse_args()
  # import IPython
  # IPython.embed()
  store = pd.HDFStore(args.output_file.name)

  comp_ext = {
    "bz2": "bz2",
    "gz": "gzip",
    "csv": None
  }
  comp = comp_ext[args.input_file.name.split('.')[-1]]


  data_file = pd.read_csv(
    args.input_file.name,
    compression=comp,
    engine='c',
    chunksize=200000,
    # iterator=True,
    parse_dates={"time": ["Timestamp"]},
    infer_datetime_format=True,
    warn_bad_lines=True,
    index_col=0
  )

  data = None

  for ticks in data_file:
    ask = ticks['Ask price'].resample('1Min', how='ohlc')
    bid = ticks['Bid price'].resample('1Min', how='ohlc')
    ask['volume'] = ticks['Ask volume'].resample('1Min', how='sum')
    bid['volume'] = ticks['Bid volume'].resample('1Min', how='sum')

    calculated = pd.concat([ask, bid], axis=1, keys=['Ask', 'Bid'])

    if data.__class__ != None.__class__:
      data = merge_chunks(data, calculated)
    else:
      data = calculated

    print data.ix[-1].name

  data.columns = ['_'.join(col).strip() for col in data.columns]
  data["volume"] = data["Bid_volume"] + data["Ask_volume"]
  data.drop(["Bid_volume", "Ask_volume"], axis=1, inplace=True)

  store.put("ticks_ohlcv", data)


def merge_chunks(old, new):
  """
  Merge two OHLCV dataframes
  """

  new_fixed = new.ix[1:]
  old.ix[-1] = merge_ohlcv(old.ix[-1], new.ix[0])
  return old.append(new_fixed, verify_integrity=True)

def merge_ohlcv(old, new):
  """

  Merge two OHLCV candlesticks that have overlapping keys

  """
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
