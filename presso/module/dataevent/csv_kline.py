import numpy

from presso.core.abstract.dataevent import AbstractDataEvent
from presso.core.event import CandleStickEvent


class CsvKlineDataEvent(AbstractDataEvent):
    def _init(self):
        self.__data = numpy.loadtxt(self._datapath, delimiter=',')

    async def _iter(self):
        i = 0
        for data in self.__data:
            i = i+1
            if i == 5:
                break
            bar = CandleStickEvent(data[0])
            bar.data = {'date': data[0],
                        'open': data[1],
                        'high': data[2],
                        'low': data[3],
                        'close': data[4],
                        'volume': data[5],
                        }
            yield bar
