from presso.core.abstract.portfolio import AbstractPortfolio
from presso.core.util.constants import OPERATION, TICKER, SIDE
from presso.core.util import LOG


class SimplePortfolio(AbstractPortfolio):
    def _init(self):
        pass

    def onTickerSignal(self, transaction):
        #LOG.info("Tick event")
        pass

    def onCheckOrderSignal(self, transaction):
        transaction.operation = OPERATION.CHECK_ORDERS
        self._execute(self._connector, transaction)

    def onPrinterSignal(self, transaction):
        #if not self._can_trade():
        #    LOG.info("cannot trade - trade flag is set to zero")
        #    return

        if transaction.signal > 0 and self._positions[self._quote] > 0:
            transaction.side = SIDE.BUY
            transaction.buy = self._base
            transaction.sell = self._quote
            transaction.amount = self._positions[self._quote]
            transaction.total = 1.0 / transaction.price * transaction.amount
            transaction.operation = OPERATION.BUY_MARKET
        elif transaction.signal < 0 and self._positions[self._base]> 0:
            transaction.side = SIDE.SELL
            transaction.buy = self._quote
            transaction.sell = self._base
            transaction.amount = self._positions[self._base]
            transaction.total = transaction.price * transaction.amount
            transaction.operation = OPERATION.SELL_MARKET
        else:
            # nothing todo
            return

        self._execute(self._connector, transaction)
