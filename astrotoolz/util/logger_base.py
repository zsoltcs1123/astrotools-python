import logging
from abc import ABC


class LoggerBase(ABC):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
