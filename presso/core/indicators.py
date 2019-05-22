from abc import ABC, abstractmethod
import numpy as np
from talib.abstract import *

INDICATORS = {
    'sma': lambda name, config: SMAIndicator(name, config)
}


class Indicator(ABC):
    def __init__(self, name, config):
        self._name = name
        self._config = config
        pass

    @abstractmethod
    def compute(self, input):
        raise NotImplementedError


class SMAIndicator(Indicator):
    def __init__(self, name, config):
        super().__init__(name, config)
        self.__n = self._config['n']

    def compute(self, input):
        if self._name not in input:
            input[self._name] = np.array([], dtype=float)

        output = SMA(input, timeperiod=self.__n)
        input[self._name] = np.append(input[self._name], output[-1])


class BBANDSIndicator(Indicator):
    def __init__(self, name, config):
        super().__init__(name, config)
        self.__n = self._config['n']
        self.__up_dev = self._config['dev']
        self.__down_dev = self._config['dev']

    def compute(self, input):
        if self._name not in input:
            input[self._name] = {
                'upper': np.array([], dtype=float),
                'middle': np.array([], dtype=float),
                'lower': np.array([], dtype=float),
            }

        upper, middle, lower = BBANDS(
            input, timeperiod=self.__n, nbdevup=self.__up_dev, nbdevdn=self.__down_dev)
        input[self._name] = {
            'upper': np.append(input[self._name]['upper'], upper[-1]),
            'middle': np.append(input[self._name]['middle'], middle[-1]),
            'lower': np.append(input[self._name]['lower'], lower[-1])
        }
