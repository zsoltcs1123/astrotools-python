
from dataclasses import dataclass
from datetime import datetime

from zodiac.mapped_position import MappedPosition


@dataclass
class Event:
    position1: MappedPosition
    position2: MappedPosition


@dataclass
class DecanChange(Event):
    def __repr__(self) -> str:
        f'{self.position2.planet} Decan change at {self.position2.time}: {self.position1.decan} -> {self.position2.decan}'

    def tv_timestamp(self) -> str:
        """timestamp("2023-02-27 11:05:00")"""
        return f'timestamp(\"{self.position2.time.strftime("%Y-%m-%d %H:%M:%S")}\")'


@dataclass
class TermChange(Event):
    def __repr__(self) -> str:
        f'{self.position2.planet} Term change at {self.position2.term}: {self.position1.decan} -> {self.position2.term}'
