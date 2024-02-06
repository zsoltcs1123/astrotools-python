from abc import ABC

from astrotoolz.util.console_logger import ConsoleLogger


class LoggerBase(ABC):
    def __init__(self):
        self._logger = ConsoleLogger(self.__class__.__name__)
