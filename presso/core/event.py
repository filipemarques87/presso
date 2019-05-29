import math
import time


class Event:
    def __init__(self, type, date=None, data=None):
        self.type = type
        self.date = date
        if not self.date:
            self.date = math.ceil(time.time())
        self.data = data
