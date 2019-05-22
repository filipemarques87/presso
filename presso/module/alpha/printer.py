import random 

from presso.core.abstract.alpha_ta import AbstractAlphaTA


class PrinterAlpha(AbstractAlphaTA):
    def _init(self):
        pass

    async def _computeSignal(self):
        print(self._df['sma20'])
        return (random.random() - 0.5) * 2
