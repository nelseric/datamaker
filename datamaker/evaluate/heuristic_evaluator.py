"Heuristic Evaluators"

from datamaker.evaluate import Evaluator

from datamaker.backtest import MarketOrder
import random

class HeuristicEvaluator(Evaluator):

    """docstring for HeuristicEvaluator"""
    def __init__(self, prediction_data, **kwargs):
        super(HeuristicEvaluator, self).__init__(**kwargs)
        self.prediction_data = prediction_data

    def evaluate_market(self, market, time):
        if len(market.open_orders) == 0:
            if self.prediction_data.ix[time]["1"] > 0.72:
                new_order = MarketOrder(
                    side=self.side,
                    take_profit=self.take_profit,
                    stop_loss=self.stop_loss,
                    size=1000
                )
                market.place_order(new_order)
