from abc import ABC, abstractmethod

class AbstractReport(ABC):
    """
    Used to report transaction.
    """
    def __init__(self, config):
        self._config = config
        self._init()

    @abstractmethod
    def _init(self):
        raise NotImplementedError

    def report(self, transaction):
        #self._generate_report(transaction.get_readable_format())
        pass
        
    @abstractmethod
    def _generate_report(self, msg):
        raise NotImplementedError
