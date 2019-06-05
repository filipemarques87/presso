import math
import time


class Event:
    """
    This class defines an event that is trigger by a dataevent and caught in alpha.
    Dependent on the event type, the alpha may or not run in order.

    The parameters are:
    - type: event type
    - date: date when the event occured
    - price: the last price of the event (example, the close price if the event is related to candlestick bars)
    - data: an object that is passed to the strategies
    """

    def __init__(self, type, date=None, price=0.0, data=None):
        self.type = type
        self.date = date
        if not self.date:
            self.date = math.ceil(time.time())
        self.price = price
        self.data = data
