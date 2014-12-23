from pathlib import Path

import pandas as pd
import numpy as np

import IPython
import random


class Backtest(object):
  """Backtest runner"""
  def __init__(self, historical_data, strategy, market):
    super(Backtest, self).__init__()
    self.historical_data = historical_data
    self.strategy = strategy
    self.market = market

  def run(self):
    for time in self.market:
      self.strategy.evaluate_market(self.market, time)

    
class Market(object):
  """A Market simulation for one currency pair"""
  def __init__(self, historical, instrument, account_size, leverage):
    super(Market, self).__init__()
    self.historical = historical
    self.instrument = instrument
    self.account_size = account_size
    self.leverage = leverage

    self.orders = []

  def place_order(self, order):
    self.orders.append(order)

  def place_orders(self, time):
    for order in self.orders:
      if not order.placed:
        order.placed = True
        order.open = True        
        if order.side == "buy":
          order.price = self.historical.ix[time].closeAsk
        elif order.side == "sell":
          order.price = self.historical.ix[time].closeBid

  def process_orders(self, time):
    for order in self.orders:
      if order.open:
        candle = self.historical.ix[time]
        if order.side == "buy":
          # print("Btp: %f < 0" % ((order.price + order.take_profit) - candle.highBid))
          # print("Bsl: %f < 0" % (candle.lowBid - (order.price - order.stop_loss)))

          if order.price + order.take_profit < candle.highBid:
            order.open = False
            order.exit_price = order.price + order.take_profit

            self.balance = self.balance + order.take_profit * order.size

          elif order.price - order.stop_loss > candle.lowBid:
            order.open = False
            order.exit_price = order.price - order.stop_loss

            self.balance = self.balance - order.stop_loss * order.size

        elif order.side == "sell":
          # print("S: %f > %f" % (order.price + order.stop_loss, candle.lowAsk))
          # print("S: %f < %f" % (order.price - order.take_profit, candle.highAsk))

          if order.price - order.take_profit > candle.lowAsk:
            order.open = False
            order.exit_price = order.price - order.take_profit

            self.balance = self.balance + order.take_profit * order.size

          elif order.price + order.stop_loss < candle.highAsk:
            order.open = False
            order.exit_price = order.price + order.stop_loss

            self.balance = self.balance - order.stop_loss * order.size




  def __iter__(self):
    self.orders = []
    self.balance = self.account_size
    self.balance_data = pd.Series(index=self.historical.index)

    for _, chunk in self.historical.groupby(np.arange(len(self.historical))//5000):
      for time in chunk.index:
        self.process_orders(time)
        yield self.historical.ix[:time]
        self.place_orders(time)
        self.balance_data[time] = self.balance
      print("%s: %2f - %d" % (chunk.index[-1], self.balance, len(self.orders)))
    

class MarketOrder(object):
  """A simulated market order"""
  def __init__(self, side, size,  take_profit, stop_loss):
    super(MarketOrder, self).__init__()
    self.side = side

    self.price = None
    self.exit_price = None
    self.size = size

    self.take_profit = take_profit
    self.stop_loss = stop_loss
    self.placed = False
    self.open = False
  
  def __repr__(self):
    if not self.placed:
      return "%s: %0f (%f/%f)" % (self.side, self.size, self.take_profit, self.stop_loss)
    elif self.open:
      return "%s %0f @ %f (%f/%f)" % (self.side, self.size, self.price, self.take_profit, self.stop_loss)
    else:
      if self.side == "buy":
        return "Buy %0f %f (%f)" % (self.size, (self.exit_price - self.price), (self.exit_price - self.price) * self.size)
      else:
        return "Sell %0f %f (%2f)" % (self.size, -(self.exit_price - self.price), -(self.exit_price - self.price) * self.size)
