from presso.core.util.constants import EVENT_TYPE


class Event:
    def __init__(self, date, etype):
        self.datetime = date
        self.type = etype
        self.data = None


class CheckOrderEvent(Event):
    def __init__(self, date):
        super().__init__(date, EVENT_TYPE.CHECK_ORDERS)


class TickEvent(Event):
    def __init__(self, date):
        super().__init__(date, EVENT_TYPE.TICK)


class CandleStickEvent(Event):
    def __init__(self, date):
        super().__init__(date, EVENT_TYPE.CANDLE_STICK)
