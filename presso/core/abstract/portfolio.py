import asyncio
from abc import ABC, abstractmethod
import functools

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
        for rpt in self._reports.values():
            rpt.report(transaction)
        
        self._transactions.append(transaction)
        task = asyncio.ensure_future(connector.execute(transaction))
        def __callback(fn):
            if fn.cancelled():
                LOG.warn("Connector call canceled")
            elif fn.done():
                error = fn.exception()
                if error:
                    LOG.critical("Error on connector call: args:{}, result:{}".format(fn.arg, error))
                else:
                    tr = fn.result()
                    print("****")
                    print(str(tr))

        task.add_done_callback(__callback)

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
