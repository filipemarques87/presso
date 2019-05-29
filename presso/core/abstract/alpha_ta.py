from abc import abstractmethod
import numpy as np
# import pandas as pd
#from talib.abstract import *
from abc import ABC, abstractmethod

from presso.core.abstract.alpha import AbstractAlpha
from presso.core.indicators import INDICATORS
from presso.core.util.constants import EVENT

OHLC_HEADER = ['date', 'open', 'high', 'low', 'close', 'volume']


class AbstractAlphaTA(AbstractAlpha):
    def __init__(self, name, portfolio, evts, config):
        super().__init__(name, portfolio, evts, config)

        self.__n = self._config['n']
        self._df = dict((k, np.full(self.__n, np.nan, dtype=float)) for k in OHLC_HEADER)
        self.__indicators = dict((ind['name'], self.__get_indicator(ind))
                                 for ind in self._config['indicators'])

    def _init(self):
        pass

    async def _calcSignal(self, data, type):
        if type == EVENT.HISTO_DATA:
            for candle in data:
                for k in OHLC_HEADER:
                    self._df[k] = self.__shift5(self._df[k], -1)
                    self._df[k][-1] = candle[k]
            return -10

        for k in OHLC_HEADER:
            self._df[k] = self.__shift5(self._df[k], -1)
            self._df[k][-1] = data[k]
        
        for ind in self.__indicators:
            self._df[ind] = self.__indicators[ind].compute(self._df)
        return await self._computeSignal(type)

    # https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    def __shift5(self, arr, num, fill_value=np.nan):
        result = np.empty_like(arr)
        if num < 0:
            result[num:] = fill_value
            result[:num] = arr[-num:]
        elif num > 0:
            result[:num] = fill_value
            result[num:] = arr[:-num]
        else:
            result = arr
        return result

    @abstractmethod
    async def _computeSignal(self, type):
        raise NotImplementedError

    def __get_indicator(self, ind):
        ind_type = ind['type']
        if ind_type not in INDICATORS:
            raise Exception('Indicator not recognized: %s' % (ind_type))
        return INDICATORS[ind_type](ind['name'], ind['config'])
