import numpy
import sqlite3

from presso.core.abstract.dataevent import AbstractDataEvent
from presso.core.event import CandleStickEvent, TickEvent


class SQLiteKlineDataEvent(AbstractDataEvent):
    def _init(self):
        self.__conn = sqlite3.connect(self._datapath)
        self.__cursor = self.__conn.cursor()
        self.__query = self._config['query']

        # execute the query
        self.__cursor.execute(self.__query)

    async def _iter(self):
        while True:
            data = self.__cursor.fetchone()
            if data is None:
                break

            bar = None
            if data[2] == '1':
                bar = TickEvent(data[0])
                bar.price = data[6]
            else:
                bar = CandleStickEvent(data[0])
                bar.data = {'date': data[0],
                            'open': data[3],
                            'high': data[4],
                            'low': data[5],
                            'close': data[6],
                            'volume': data[7],
                            }

            yield bar

    def shutdown(self):
        super().shutdown()
        self.__conn.close()
