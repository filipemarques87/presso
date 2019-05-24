from presso.core.util.constants import EVENT_TYPE


class Event:
    def __init__(self, date, etype):
        self.datetime = date
        self.type = etype


class TickEvent(Event):
    def __init__(self, date):
        super().__init__(date, EVENT_TYPE.TICK)
        self.price = 0


class CandleStickEvent(Event):
    def __init__(self, date):
        super().__init__(date, EVENT_TYPE.CANDLE_STICK)
        self.data = None
