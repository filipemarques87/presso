import asyncio
from abc import ABC, abstractmethod
import redis

from presso.core.util.constants import STATUS
from presso.core.util import LOG, REDIS_DB


class AbstractPortfolio(ABC):
    def __init__(self, connectors, reports, statistics, config):
        self._connectors = connectors
        self._reports = reports
        self._statistics = statistics
        self._config = config
        self._transactions = []
        self._base = config["base"]
        self._quote = config["quote"]
        self._init()

    def _execute(self, connector, transaction):
        # report the transaction
        for r in self._reports:
            self._reports[r].report(transaction)
        
        self._transactions.append(transaction)
        task = asyncio.ensure_future(connector.execute(transaction))
        def __callback(_, tr):
            pass
            #if transaction.status == STATUS.SUCCESS:
            #    self._positions[transaction.buy] += transaction.amount
            #    self._positions[transaction.sell] -= transaction.total
            #    transaction.portfolio = self._positions.copy()
        task.add_done_callback(__callback, transaction)

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

    def _get_position(self, ticker):
        return float(self.__get_from_redis("qb:pos:%s" % (ticker)))

    def _set_position(self, ticker, balance):
        REDIS_DB.set("qb:pos:%s" % (ticker), str(balance))

    def _can_trade(self):
        return int(self.__get_from_redis("qb:cantrade")) == 1
