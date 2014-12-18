#!/usr/bin/env python

from database import *

import oandapy
import dotenv
import os
import datetime

import ext.oandapy


class HistoricalIterator(object):
  """docstring for HistoricalIterator"""
  def __init__(self, instrument, years, granularity = "M1", chunk_size=5000):
    self.instrument = instrument
    self.granularity = granularity
    self.chunk_size = chunk_size

    self.data_range = datetime.timedelta(365.25 * years)
    self.data_start = datetime.datetime.now() - self.data_range
    self.cur_date = self.data_start.isoformat()

    self.first_chunk = True
    self.no_more_chunks = False

    dotenv.load_dotenv('.env')
    oanda_token = os.environ.get("OANDA_TOKEN", "")
    oanda_env = os.environ.get("OANDA_ENV", "")
    self.oanda = oandapy.API(environment=oanda_env, access_token=oanda_token)

  def __iter__(self):
    return self

  def get_chunk(self):
    if self.no_more_chunks:
      raise StopIteration()

    cur = self.oanda.get_history(instrument=self.instrument,
                            granularity=self.granularity,
                            count=self.chunk_size,
                            start=self.cur_date)

    if len(cur['candles']) < self.chunk_size:
      self.no_more_chunks = True

    if not self.first_chunk:
      cur["candles"] = cur["candles"][1:]
    self.first_chunk = False

    # Tracer()()
    self.cur_date = cur["candles"][-1]["time"]

    return Chunk(cur)

  def next(self):
    return self.get_chunk()

class Chunk(object):
  def __init__(self, chunk_data):
    self.instrument = chunk_data["instrument"]
    self.granularity = chunk_data["granularity"]
    self.candles = chunk_data["candles"]

  def __iter__(self):
    return iter(self.candles)

  def __repr__(self):
    return "<Chunk('%s' '%s' ['%s' : '%s']x%s)>" % (
      self.instrument, self.granularity,
      self.candles[0]["time"], self.candles[-1]["time"],
      len(self.candles))
