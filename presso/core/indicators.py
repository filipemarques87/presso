from abc import ABC, abstractmethod
from talib.abstract import *

INDICATORS = {
    'sma': lambda name, config: SMAIndicator(name, config)
}


class Indicator(ABC):
    """
    The Indicator class is a wrapper class to use the indicators from ta-lib.
    Those indicators must be defined in config file and they are available in all alpha's
    classes that extends from AbstractAlphaTA class.
    """

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
        return SMA(input, timeperiod=self.__n)


class BBANDSIndicator(Indicator):
    def __init__(self, name, config):
        super().__init__(name, config)
        self.__n = self._config['n']
        self.__up_dev = self._config['dev']
        self.__down_dev = self._config['dev']

    def compute(self, input):
        upper, middle, lower = BBANDS(
            input, timeperiod=self.__n, nbdevup=self.__up_dev, nbdevdn=self.__down_dev)
        input[self._name] = {
            'upper': upper,
            'middle': middle,
            'lower': lower
        }
