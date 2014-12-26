"Naive Strategies"

from datamaker.strategy import Strategy

from datamaker.backtest import MarketOrder
import random


class NaiveRandom(Strategy):

    def evaluate_market(self, market, time):
        if len([order for order in market.orders if order.open]) == 0:
            new_order = MarketOrder(
                side=random.choice(["buy", "sell"]),
                take_profit=100 * 0.0001,
                stop_loss=100 * 0.0001,
                size=random.randrange(100, 10000)
            )
            market.place_order(new_order)


class NaiveBuy(Strategy):

    def evaluate_market(self, market, time):
        if len([order for order in market.orders if order.open]) == 0:
            new_order = MarketOrder(
                side="buy",
                take_profit=100 * 0.0001,
                stop_loss=100 * 0.0001,
                size=1000
            )
            market.place_order(new_order)


class NaiveSell(Strategy):

    def evaluate_market(self, market, time):
        if len([order for order in market.orders if order.open]) == 0:
            new_order = MarketOrder(
                side=random.choice("sell"),
                take_profit=100 * 0.0001,
                stop_loss=100 * 0.0001,
                size=1000
            )
            market.place_order(new_order)
