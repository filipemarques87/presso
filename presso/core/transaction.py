from datetime import datetime

from presso.core.util.constants import OPERATION


class Transaction:
    def __init__(self):
        self.tstamp = 0  # time stamp of the transaction
        self.id = None  # the id of transaction after place an order to the broker
        self.signal = 0  # the strength of the action: -1 to sell and 1 to buy
        self.side = None  # the way of the transaction: can be SELL or BUY
        self.price = 0  # last price that is used to calculate the positions to transaction
        self.amount = 0  # amount to buy or sell
        self.total = 0  # total value of the transaction (price * amount)
        self.operation = None  # operation type: buy market, buy limit, ...
        # status of the transaction
        # when an order is placed into the market, the status is set to PENDING
        # and when the order is comleted, the status is set to COMPLETED
        self.status = None
        self.to_cancel = False # indicates if this transaction needs to cancel all trades before buy sell

    def __str__(self):
        return '%f,%s,%f,%s,%f,%f,%f,%s,%s,%d' % (
            self.tstamp,
            self.id,
            self.signal,
            self.side,
            self.price,
            self.amount,
            self.total,
            str(self.operation),
            str(self.status),
            self.to_cancel)
