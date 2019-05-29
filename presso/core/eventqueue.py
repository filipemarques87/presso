from asyncio import Lock, PriorityQueue, sleep, wait_for

from presso.core.event import Event
from presso.core.util import isRealtime, LOG
from presso.core.util.constants import MAX_TIMEOUT


class EventQueue:
    __queue = None

    def __init__(self):
        self.__locker = {}
        self.__queue = PriorityQueue()

    async def consume(self):
        while True:
            _, caller, evt = await self.__queue.get()
            wait_for(caller.sendData(evt), MAX_TIMEOUT)
            if caller in self.__locker:
                self.__locker[caller].release()
                if not isRealtime():
                    # Wait for the lock to be locked
                    while not self.__locker[caller].locked():
                        await sleep(0.001)
                        if caller not in self.__locker:
                            break

    async def put(self, caller, evt):
        if not isinstance(evt, Event):
            LOG.critical("Expect class event.Event but got %s" % (str(evt.__class__)))
            return

        if caller not in self.__locker:
            self.__locker[caller] = Lock()
        await self.__locker[caller]
        self.__queue.put_nowait((evt.date, caller, evt))

    def remove(self, caller):
        self.__locker.pop(caller)

    @staticmethod
    def getInstance():
        if not EventQueue.__queue:
            EventQueue.__queue = EventQueue()
        return EventQueue.__queue
