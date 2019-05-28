import random 

from presso.core.abstract.alpha_ta import AbstractAlphaTA


class PrinterAlpha(AbstractAlphaTA):
    def _init(self):
        pass

    async def _computeSignal(self, type):
        smadf = self._df['sma20']
        closedf = self._df['close']

        signal = 0
        if smadf[-2] < closedf[-2] and smadf[-1] > closedf[-1]:
            signal = 1
        elif smadf[-2] > closedf[-2] and smadf[-1] < closedf[-1]:
            signal = -1

        return signal
