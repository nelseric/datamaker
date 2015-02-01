"""Abstract Evaluator"""

__all__ = ['naive']


class Evaluator(object):

    """ Evaluator """

    def __init__(self, take_profit, stop_loss, side):
        super(Evaluator, self).__init__()
        self.side = side
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def evaluate_market(self, market, time):
        """ Common interface for all evaluators to use when backtesting or ordering """
        raise NotImplementedError("Your indicator must define this")

    def __repr__(self):
        return ("<{0.__class__.__name__} side={0.side}, " +
                "tp={0.take_profit:0.4f}, sl={0.stop_loss:0.4f}>").format(self)
