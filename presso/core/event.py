import math
import time


class Event:
    def __init__(self, type, date=None, data=None):
        self.type = type
        self.date = not date if date else math.ceil(time.time())
        self.data = data
