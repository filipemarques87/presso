from presso.core.abstract.report import AbstractReport

class CSVReport(AbstractReport):
    def __ini__(self, config):
        super().__init__(config)
        self.__file = None

    def _init(self):
        pass

    def _generate_report(self, msg):
        pass
        #print(msg)
        
