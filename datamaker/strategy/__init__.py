"""Abstract Strategy"""


class Strategy(object):

    """ Strategy """

    def __init__(self, market, take_profit, stop_loss, *args, **kwargs):
        super(Strategy, self).__init__()
        self.market = market
        self.side = kwargs.get('side')
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def __repr__(self):
        return "<%s side=%s, tp=%d, sl=%d" % (self.__class__.__name__, self.side, self.take_profit, self.stop_loss)
