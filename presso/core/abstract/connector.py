from abc import ABC, abstractmethod
from asyncio import wait_for

from presso.core.util.constants import OPERATION
from presso.core.util import LOG


class AbstractConnector(ABC):
    def __init__(self, name, config):
        self._name = name
        self._config = config
        self._init()

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    async def execute(self, transaction):
        #LOG.info("[TR] %s" % str(transaction))
        if transaction.operation == OPERATION.SELL_LIMIT:
            transaction = self._sell_limit(transaction)
        elif transaction.operation == OPERATION.BUY_LIMIT:
            transaction = self._buy_limit(transaction)
        elif transaction.operation == OPERATION.SELL_MARKET:
            transaction = self._sell_market(transaction)
        elif transaction.operation == OPERATION.BUY_MARKET:
            transaction = self._buy_market(transaction)
        elif transaction.operation == OPERATION.CANCEL_ALL_ORDERS:
            transaction = self._cancel_all_orders(transaction)
        elif transaction.operation == OPERATION.CHECK_ORDERS:
            transaction = self._get_order_status(transaction)

        return transaction

    @abstractmethod
    def _buy_limit(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def _sell_limit(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def _buy_market(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def _sell_market(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def _cancel_order(self, transaction):
        raise NotImplementedError

    @abstractmethod
    def _cancel_all_orders(self, transaction):
        raise NotImplementedError

    

    #def get_order_book(symbol):
    #def get_order(symbol, orderId):
    @abstractmethod
    def _get_order_status(self, transaction):
        raise NotImplementedError
