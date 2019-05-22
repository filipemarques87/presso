import numpy
import sqlite3

from presso.core.abstract.dataevent import AbstractDataEvent


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

            #yield data
            yield [data[0],
                   {'date': data[0],
                    'symbol': data[1],
                    'open': data[3],
                    'high': data[4],
                    'low': data[5],
                    'close': data[6],
                    'volume': data[7],
                    }]

    def shutdown(self):
        super().shutdown()
        self.__conn.close()
