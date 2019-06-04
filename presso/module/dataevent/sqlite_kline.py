import numpy
import sqlite3
import time

from presso.core.abstract.dataevent import AbstractDataEvent
from presso.core.event import Event
from presso.core.util.constants import EVENT


class SQLiteKlineDataEvent(AbstractDataEvent):
    def _init(self):
        self.__conn = sqlite3.connect(self._datapath)
        self.__cursor = self.__conn.cursor()
        self.__query = self._config['query']

        # execute the query
        self.__cursor.execute(self.__query)

    def _init_histo_data(self, n):
        edata = []
        count = 0
        while count < n:
            data = self.__cursor.fetchone()
            if data[2] == 1:
                continue
            edata.append({'date': data[0]/1000,
                          'open': data[3],
                          'high': data[4],
                          'low': data[5],
                          'close': data[6],
                          'volume': data[7]
                          })
            count = count+1
        return Event(EVENT.HISTO_DATA, data=edata) 

    async def _iter(self):
        check_order = False
        while True:
            #time.sleep(0.05)

            etype = None
            tstamp = -1
            edata = None
            if check_order:
                check_order = False
                etype = EVENT.CHECK_ORDERS
            else:
                check_order = True
                data = self.__cursor.fetchone()
                if data is None:
                    break

                tstamp = data[0]/1000
                etype = EVENT.TICK if data[2] == 1 else EVENT.CANDLE_STICK
                edata = {'date': tstamp,
                         'open': data[3],
                         'high': data[4],
                         'low': data[5],
                         'close': data[6],
                         'volume': data[7]
                         }

            yield Event(etype, date=tstamp, price=data[6], data=edata)

    def shutdown(self):
        super().shutdown()
        self.__conn.close()
