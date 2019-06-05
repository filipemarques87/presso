from enum import Enum


MAX_TIMEOUT = 1

# order side relatively to base currency
SIDE = Enum("SIDE", ("SELL", "BUY"))

# transaction status
STATUS = Enum('STATUS', ('SUCCESS', 'FAIL', 'PENDING','CANCELED'))

# operation type
OPERATION = Enum('OPERATION', ('SELL_LIMIT', 'BUY_LIMIT',
                               'SELL_MARKET', 'BUY_MARKET', 'CANCEL_ALL_ORDERS', 'CHECK_ORDERS'))

# the events are user defined in file configuration
EVENT = Enum('EVENT', ('HISTO_DATA'))


