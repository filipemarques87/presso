from abc import abstractmethod
import numpy as np
# import pandas as pd
#from talib.abstract import *
from abc import ABC, abstractmethod

from presso.core.abstract.alpha import AbstractAlpha
from presso.core.indicators import INDICATORS

OHLC_HEADER = ['date', 'open', 'high', 'low', 'close', 'volume']


class AbstractAlphaTA(AbstractAlpha):
    def __init__(self, name, portfolio, main_dataevent, dataevents, evts, config):
        super().__init__(name, portfolio, main_dataevent, dataevents, evts, config)
        self._df = dict((k, np.array([], dtype=float)) for k in OHLC_HEADER)
        self.__indicators = dict((ind['name'], self.__get_indicator(ind))
                                 for ind in self._config['indicators'])

    def _init(self):
        pass

    async def _calcSignal(self, data):
        for k in OHLC_HEADER:
            self._df[k] = np.append(self._df[k], data[k])

        dict((ind, self.__indicators[ind].compute(self._df))
             for ind in self.__indicators)
        return await self._computeSignal()

    @abstractmethod
    async def _computeSignal(self):
        raise NotImplementedError

    def __get_indicator(self, ind):
        ind_type = ind['type']
        if ind_type not in INDICATORS:
            raise Exception('Indicator not recognized: %s' % (ind_type))
        return INDICATORS[ind_type](ind['name'], ind['config'])
