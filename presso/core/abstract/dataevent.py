import asyncio

from abc import ABC, abstractmethod

import numpy

from presso.core.eventqueue import EventQueue
from presso.core.transaction import Transaction
from presso.core.util import LOG


class AbstractDataEvent(ABC):
    def __init__(self, datapath, historyfile, config):
        self._datapath = datapath
        self._historyfile = historyfile
        self._config = config
        self._alphas = set()
        self._history = None
        self._task = asyncio.ensure_future(self._start())
        self._init()

    def addAlpha(self, alpha):
        self._alphas.add(alpha)

    def sendData(self, evt):
        self._saveHistory(evt)
        transaction = Transaction()
        transaction.tstamp = evt.date
        tasks = [alpha.onData(transaction, evt) for alpha in self._alphas]
        return asyncio.gather(*tasks)

    def _saveHistory(self, data):
        pass
        #if self._history is None:
        #    self._history = [data]
        #else:
        #    self._history = numpy.vstack([self._history, data])

    def shutdown(self):
        if self._task.done() and self._task.exception():
            LOG.error(self._task.exception())
        self._task.cancel()
        if self._historyfile and self._history is not None:
            numpy.save(self._historyfile, self._history)

    async def _start(self):
        event_queue = EventQueue.getInstance()
        # get historic data for initialization
        evt = self._init_histo_data(self._config["init_n"])
        await event_queue.put(self, evt)

        # start with realtime
        async for evt in self._iter():
            # Wait for previous event to be consumed
            await event_queue.put(self, evt)
        event_queue.remove(self)

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    @abstractmethod
    async def _iter(self):
        raise NotImplementedError
    
    @abstractmethod
    def _init_histo_data(self, n):
        """
        This method is used to initialize the stretagies with past data (for example
        used to initialize the arrays to compute the technical analysis indicators)
        """
        raise NotImplementedError
