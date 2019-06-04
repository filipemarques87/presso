import asyncio
from abc import ABC, abstractmethod
import functools

from presso.core.util.constants import STATUS, SIDE
from presso.core.util import LOG, REDIS_DB


class AbstractPortfolio(ABC):
    def __init__(self, connector, reports, statistics, config):
        self._connector = connector
        self._reports = reports
        self._statistics = statistics
        self._config = config
        self._base = config["base"]
        self._quote = config["quote"]
        self._transactions = []
        self._pending_trans = []  # transactions to be checked
        self._positions = {}
        self._holds = {}
        self.__read_positions()
        self._init()

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    def _execute(self, connector, transaction):
        def __callback(fn):
            if fn.cancelled():
                LOG.warn("Connector call canceled")
            elif fn.done():
                error = fn.exception()
                if error:
                    LOG.critical(
                        "Error on connector call: args:{}, result:{}".format(fn.arg, error))
                else:
                    transactions = fn.result()
                    if transactions is None:
                        return
                    # the variable tr can be a scalar (unique trasanction)
                    # or can be an array of transaction (for example a confirmation of
                    # multi transactions)
                    if not isinstance(transactions, list):
                        transactions = [transactions]

                    # transactions report
                    for tr in transactions:
                        for rpt in self._reports.values():
                            rpt.report(tr)

                        if tr.status == STATUS.PENDING:
                            self.__update_positions_on_pending(tr)
                        elif tr.status == STATUS.SUCCESS:
                            self.__update_positions_on_success(tr)
                        elif tr.status == STATUS.CANCELED:
                            self.__update_positions_on_cancel(tr)

                    self.__save_positions()

        task = asyncio.ensure_future(connector.execute(transaction))
        task.add_done_callback(__callback)

    def __update_positions_on_pending(self, transaction):
        '''
        Append this transaction into pending transaction list
        and transfer the positions from position list to hold one.
        The holds positions are not available to transaction.
        '''
        buy, sell = self.__get_buy_sell(transaction.side)
        self._positions[sell] -= transaction.amount
        self._holds[buy] += transaction.total
        self._pending_trans.append(transaction)

    def __update_positions_on_success(self, transaction):
        '''
        Append this transactions list and transfer the positions previous
        held into the postions.
        Until here, the buy positions are not available.
        '''
        buy, sell = self.__get_buy_sell(transaction.side)
        pend_tr_idx = self.__get_pending_transaction(transaction)
        self._positions[sell] -= (transaction.amount -
                                   self._pending_trans[pend_tr_idx].amount)
        self._positions[buy] += transaction.total


        self._holds[buy] -= self._pending_trans[pend_tr_idx].total

        self.__remove_pending_transaction(transaction)
        self._transactions.append(transaction)

    def __update_positions_on_cancel(self, transaction):
        '''
        Restores the positions on a cancel result. The hold positions
        are trabsferred back to positions.
        '''
        _, sell = self.__get_buy_sell(transaction.side)
        self._positions[sell] += transaction.amount
        self.__remove_pending_transaction(transaction)
        # self._transactions.append(transaction)

    def __get_pending_transaction(self, transaction):
        pend_tr = [i for i, tr in enumerate(
            self._pending_trans) if tr.id == transaction.id]
        if not pend_tr or len(pend_tr) != 1:
            raise Exception("Expect on element")
        return pend_tr[0]

    def __remove_pending_transaction(self, transaction):
        del self._pending_trans[self.__get_pending_transaction(transaction)]

    def __get_buy_sell(self, side):
        if side == SIDE.BUY:
            return self._base, self._quote
        elif side == SIDE.SELL:
            return self._quote, self._base

    def __save_positions(self):
        '''
        Stores the positions/holds into redis
        '''
        for ticker in [self._base, self._quote]:
            REDIS_DB.set("qb:pos:%s" % (ticker), str(self._positions[ticker]))
            REDIS_DB.set("qb:hold:%s" % (ticker), str(self._holds[ticker]))

    def __read_positions(self):
        '''
        Read positions from redis
        '''
        for ticker in [self._base, self._quote]:
            self._positions[ticker] = float(
                REDIS_DB.get("qb:pos:%s" % (ticker)))
            self._holds[ticker] = float(REDIS_DB.get("qb:hold:%s" % (ticker)))

    def runStatistics(self):
        for transaction in self._transactions:
            for _, stat in self._statistics.items():
                stat.onTransaction(transaction)
        for _, stat in self._statistics.items():
            stat.finish()
