from dataclasses import dataclass
from datetime import datetime
from zodiac.mapped_position import MappedPosition as mp

@dataclass
class AstroEvent:
    time: datetime #UTC

    def tv_timestamp(self) -> str:
        """eg. timestamp("2023-02-27 11:05 UTC")"""
        return f'timestamp("{self.time.strftime("%Y-%m-%d %H:%M UTC")}")'


@dataclass
class ZodiacalEvent(AstroEvent):
    previous: mp
    current: mp


@dataclass
class SignChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.base_position.dt}\t{self.current.base_position.name}\tSign change\t{self.previous.sign.name} -> {self.current.sign.name}"


@dataclass
class DecanChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.base_position.dt}\t{self.current.base_position.name}\tDecan change\t{self.previous.decan.name} -> {self.current.decan.name}"


@dataclass
class TermChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.base_position.dt}\t{self.current.base_position.name}\tTerm change\t{self.previous.term.name} -> {self.current.term.name}"


@dataclass
class DirectionChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.base_position.dt}\t{self.current.base_position.name}\tDirection change\t{self.previous.direction} -> {self.current.direction}"


@dataclass
class Progression(AstroEvent):
    mp: mp
    name: str

    def __repr__(self) -> str:
        return f"{self.time}\t{self.mp.base_position.name}\t{self.name} progression at\t{self.mp.tropical_pos}"


