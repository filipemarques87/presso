import numpy

from presso.core.abstract.connector import AbstractConnector
from presso.core.util.constants import OPERATION, STATUS, TICKER
from presso.core.util import LOG


class KlineHistoryConnector(AbstractConnector):
    def _init(self):
        self._commission = 0.9975

    def __getPrice(self):
        pass

    #async def execute(self, transaction):
    #    #if transaction.operation == OPERATION.MARKET:
    #    #    if transaction.buy == TICKER.BTC and transaction.sell == TICKER.USD:
    #    #        transaction.price = self.__getPrice()
    #    #    elif transaction.buy == TICKER.USD and transaction.sell == TICKER.BTC:
    #    #        transaction.price = 1 / self.__getPrice()
    #    #    if transaction.total:
    #    #        transaction.amount = transaction.total / transaction.price * self._commission
    #    #    elif transaction.amount:
    #    #        transaction.total = transaction.amount * transaction.price * self._commission
    #    #    transaction.status = STATUS.SUCCESS
    #    #else:
    #    #transaction.status = STATUS.FAIL
    #    print(transaction)

    def _buy_limit(self, transaction):
        print("buy limit")
        return transaction

    def _sell_limit(self, transaction):
        print("sell limit")
        return transaction

    def _buy_market(self, transaction):
        LOG.info("buy market")
        return transaction

    def _sell_market(self, transaction):
        print("sell maarket")
        return transaction

    def _cancel_order(self, transaction):
        print("cancel order")
        return transaction

    def _cancel_all_orders(self, transaction):
        print("cancel all orders")
        return transaction
