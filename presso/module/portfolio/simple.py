from presso.core.abstract.portfolio import AbstractPortfolio
from presso.core.util.constants import OPERATION, TICKER
from presso.core.util import LOG


class SimplePortfolio(AbstractPortfolio):
    def _init(self):
        pass

    def onPrinterSignal(self, transaction):
        if not self._can_trade():
            LOG.info("cannot trade - trade flag is set to zero")
            return

        if transaction.signal > 0 and self._get_position(self._quote) > 0:
            transaction.buy = self._base
            transaction.sell = self._quote
            transaction.total = self._get_position(self._quote)
            transaction.operation = OPERATION.BUY_MARKET
        elif transaction.signal < 0 and self._get_position(self._base)> 0:
            transaction.buy = self._quote
            transaction.sell = self._base
            transaction.total = self._get_position(self._base)
            transaction.operation = OPERATION.SELL_MARKET
        else:
            # nothing todo
            return

        self._execute(self._connectors['kline_history'], transaction)
