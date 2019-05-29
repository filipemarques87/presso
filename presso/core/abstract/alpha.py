from abc import ABC, abstractmethod


from presso.core.util import LOG, REDIS_DB
from presso.core.util import LOG

class AbstractAlpha(ABC):
    def __init__(self, name, portfolio, evts, config):
        self.name = name
        self._evts = evts
        self._config = config
        # Check if portfolio has handler function
        callback_name = 'on%sSignal' % self.name
        if hasattr(portfolio, callback_name):
            self._callback = getattr(portfolio, callback_name)
        else:
            raise NotImplementedError('No handler function defined in portfolio')
        self._init()

    async def onData(self, transaction, evt):
        if evt.type not in self._evts or not self._evts:
            return

        if not bool(REDIS_DB.get("qb:cantrade")):
            LOG.info("Not allowed to trade")
            return
            
        signal = await self._calcSignal(evt.data, evt.type)
        if signal > 1 or signal < -1:
            LOG.warn('Signal value should between +/-1')
            return
        transaction.signal = signal
        transaction.etype = evt.type
        self._callback(transaction)

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    @abstractmethod
    async def _calcSignal(self, data, type):
        raise NotImplementedError
