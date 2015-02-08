import numpy as np

import pandas as pd

import IPython


class Backtest(object):

    """Backtest runner"""

    def __init__(self, historical_data, evaluators, market):
        super(Backtest, self).__init__()
        self.historical_data = historical_data
        self.evaluators = evaluators
        self.market = market

    def run(self):
        for time, _ in self.market:
            for evaluator in self.evaluators:
                evaluator.evaluate_market(self.market, time)


class Market(object):

    """A Market simulation for one currency pair"""

    def __init__(self, historical, instrument, account_size, leverage):
        super(Market, self).__init__()
        self.historical = historical
        self.instrument = instrument
        self.account_size = account_size
        self.balance = account_size
        self.leverage = leverage
        self.balance_data = None

        self.pending_orders = []
        self.open_orders = []
        self.closed_orders = []

    def place_order(self, order):
        self.pending_orders.append(order)

    def place_orders(self, candle):
        for order in list(self.pending_orders):
            order.placed = True
            order.open = True
            if order.side == "buy":
                order.price = candle.closeAsk
            elif order.side == "sell":
                order.price = candle.closeBid
            self.pending_orders.remove(order)
            self.open_orders.append(order)

    def process_orders(self, candle):
        for order in list(self.open_orders):
            if order.side == "buy":
                if order.price + order.take_profit < candle.highBid:
                    order.open = False
                    self.open_orders.remove(order)
                    self.closed_orders.append(order)
                    order.exit_price = order.price + order.take_profit

                    self.balance = self.balance + \
                        order.take_profit * order.size

                elif order.price - order.stop_loss > candle.lowBid:
                    order.open = False
                    self.open_orders.remove(order)
                    self.closed_orders.append(order)
                    order.exit_price = order.price - order.stop_loss

                    self.balance = self.balance - \
                        order.stop_loss * order.size

            elif order.side == "sell":

                if order.price - order.take_profit > candle.lowAsk:
                    order.open = False
                    self.open_orders.remove(order)
                    self.closed_orders.append(order)
                    order.exit_price = order.price - order.take_profit

                    self.balance = self.balance + \
                        order.take_profit * order.size

                elif order.price + order.stop_loss < candle.highAsk:
                    order.open = False
                    self.open_orders.remove(order)
                    self.closed_orders.append(order)
                    order.exit_price = order.price + order.stop_loss

                    self.balance = self.balance - \
                        order.stop_loss * order.size

    def __iter__(self):
        self.pending_orders = []
        self.open_orders = []
        self.closed_orders = []
        self.balance = self.account_size
        self.balance_data = pd.Series(index=self.historical.index)

        for _, chunk in self.historical.groupby(
                np.arange(len(self.historical)) // 5000):
            for time, candle in chunk.iterrows():
                # IPython.embed()
                self.process_orders(candle)
                yield time, candle
                self.place_orders(candle)
                self.balance_data[time] = self.balance

            print("%s: %s" % (chunk.index[-1], self))

    def __repr__(self):
        return ("<Market({0.instrument}):{0.balance:0.2f} {1}/{2}/{3}>")\
            .format(self,
                    len(self.pending_orders),
                    len(self.open_orders),
                    len(self.closed_orders))


class MarketOrder(object):

    """A simulated market order"""

    def __init__(self, side, size, take_profit, stop_loss):
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
            return "%s: %0f (%f/%f)" % (self.side, self.size,
                                        self.take_profit, self.stop_loss)
        elif self.open:
            return "%s %0f @ %f (%f/%f)" % (self.side, self.size,
                                            self.price, self.take_profit,
                                            self.stop_loss)
        else:
            if self.side == "buy":
                return "Buy %0f %f (%f)" % (
                    self.size, (self.exit_price - self.price),
                    (self.exit_price - self.price) * self.size)
            else:
                return "Sell %0f %f (%2f)" % (
                    self.size, -(self.exit_price - self.price),
                    -(self.exit_price - self.price) * self.size)
