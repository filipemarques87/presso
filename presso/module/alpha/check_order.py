import random

from presso.core.abstract.alpha_ta import AbstractAlpha


class CheckOrderAlpha(AbstractAlpha):
    def _init(self):
        pass

    async def _calcSignal(self, data, type):
        return 0
