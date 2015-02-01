"Naive Evaluators"

from datamaker.evaluate import Evaluator

from datamaker.backtest import MarketOrder
import random


class NaiveEvaluator(Evaluator):

    def evaluate_market(self, market, time):
        if len(market.open_orders) == 0:
            new_order = MarketOrder(
                side=self.side,
                take_profit=self.take_profit,
                stop_loss=self.stop_loss,
                size=1000
            )
            market.place_order(new_order)
