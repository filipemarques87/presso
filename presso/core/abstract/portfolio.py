import asyncio
from abc import ABC, abstractmethod
import redis

from presso.core.util.constants import STATUS
from presso.core.util import LOG, REDIS_DB


class AbstractPortfolio(ABC):
    def __init__(self, connectors, statistics, config):
        self._connectors = connectors
        self._statistics = statistics
        self._config = config
        self._transactions = []

        self._init()

    def _execute(self, connector, transaction, callback=None):
        self._transactions.append(transaction)
        task = asyncio.ensure_future(connector.execute(transaction))
        #def __callback(_):
        #    if transaction.status == STATUS.SUCCESS:
        #        self._positions[transaction.buy] += transaction.amount
        #        self._positions[transaction.sell] -= transaction.total
        #        transaction.portfolio = self._positions.copy()
        task.add_done_callback(callback)

    def runStatistics(self):
        for transaction in self._transactions:
            for _, stat in self._statistics.items():
                stat.onTransaction(transaction)
        for _, stat in self._statistics.items():
            stat.finish()

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    def __get_from_redis(self, key):
        value = REDIS_DB.get(key)
        if not value:
            msg = "redis key'%s' not defined" % (key)
            LOG.critical(msg)
            raise Exception(msg)
        return value

    @property
    def base(self):
        return self.__get_from_redis("quantbot:base")

    @property
    def quote(self):
        return self.__get_from_redis("quantbot:quote")

    def _get_position(self, ticker):
        return float(self.__get_from_redis("quantbot:position:%s" % (ticker)))

    def _set_position(self, ticker, balance):
        REDIS_DB.set("quantbot:position:%s" % (ticker), str(balance))
