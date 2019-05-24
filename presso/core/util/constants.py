from enum import Enum


MAX_TIMEOUT = 1

STATUS = Enum('STATUS', ('SUCCESS', 'FAIL'))

TICKER = Enum('TICKER', ('USD', 'USDT', 'BTC',
                         'LTC', 'BCH', 'ETH', 'ADA', 'XEM'))

OPERATION = Enum('OPERATION', ('SELL_LIMIT', 'BUY_LIMIT',
                               'SELL_MARKET', 'BUY_MARKET', 'CANCEL_ALL_ORDERS'))

EVENT_TYPE = Enum('EVENT_TYPE', ('TICK', 'CANDLE_STICK'))
