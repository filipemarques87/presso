from datetime import datetime

from presso.core.util.constants import OPERATION


class Transaction:
    def __init__(self):
        self.tstamp = 0
        self.id = None
        self.signal = 0
        self.side = None
        self.price = 0
        self.amount = 0
        self.total = 0
        self.operation = None
        self.status = None
        self.portfolio = None
        self.etype = None

    # TODO - improve the readable format
    def get_readable_format(self):
        srt_date = datetime.fromtimestamp(
            self.tstamp).strftime('%d/%m/%Y %H:%M:%S')

        action = "Place order"
        if self.status is not None:
            action = "Completed order[%s]" % self.status

        order_type = "BUY"
        if self.operation == OPERATION.SELL_LIMIT or self.operation == OPERATION.SELL_MARKET:
            order_type = "SELL"
        elif self.operation == OPERATION.CANCEL_ALL_ORDERS:
            order_type = "CANCEL"

        return '%s - %s %s' % (
            srt_date,
            action,
            order_type)

    def __str__(self):
        return '%f,%s,%f,%s,%f,%f,%f,%s,%s,%s,%s' % (
            self.tstamp,
            self.id,
            self.signal,
            self.side,
            self.price,
            self.amount,
            self.total,
            str(self.operation),
            str(self.status),
            str(self.portfolio),
            str(self.etype))
