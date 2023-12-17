from dataclasses import dataclass
from datetime import datetime
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition as mp


@dataclass
class AstroEvent:
    dt: datetime  # UTC

    def tv_timestamp(self) -> str:
        """eg. timestamp("2023-02-27 11:05 UTC")"""
        return f'timestamp("{self.dt.strftime("%Y-%m-%d %H:%M UTC")}")'


@dataclass
class ZodiacalEvent(AstroEvent):
    previous: mp
    current: mp


@dataclass
class TropicalSignChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tSign change\t{self.previous.tropical.sign.name} -> {self.current.tropical.sign.name}"

    def label(self) -> str:
        return f"{self.current.point} TropicalSignChange {self.previous.tropical.sign.name} -> {self.current.tropical.sign.name}"


@dataclass
class VedicSignChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tSign change\t{self.previous.vedic.sign.name} -> {self.current.vedic.sign.name}"

    def label(self) -> str:
        return f"{self.current.point} VedicSignChange {self.previous.vedic.sign.name} -> {self.current.vedic.sign.name}"


@dataclass
class DecanChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tDecan change\t{self.previous.tropical.decan.name} -> {self.current.tropical.decan.name}"

    def label(self) -> str:
        return f"{self.current.point} DecanChange {self.previous.tropical.decan.name} -> {self.current.tropical.decan.name}"


@dataclass
class TermChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tTerm change\t{self.previous.tropical.term.name} -> {self.current.tropical.term.name}"

    def label(self) -> str:
        return f"{self.current.point} TermChange {self.previous.tropical.term.name} -> {self.current.tropical.term.name}"


@dataclass
class NakshatraChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tNakshatra change\t{self.previous.vedic.nakshatra.name} -> {self.current.vedic.nakshatra.name}"

    def label(self) -> str:
        return f"{self.current.point} NakshatraChange {self.previous.vedic.nakshatra.name}[{self.previous.vedic.nakshatra.ruler}] -> {self.current.vedic.nakshatra.name}[{self.current.vedic.nakshatra.ruler}]"


@dataclass
class DirectionChange(ZodiacalEvent):
    def __repr__(self) -> str:
        return f"{self.current.dt}\t{self.current.point}\tDirection change\t{self.previous.direction} -> {self.current.direction}"

    def label(self) -> str:
        return f"{self.current.point} DirectionChange {self.previous.direction} -> {self.current.direction}"


@dataclass
class TropicalProgression(AstroEvent):
    mp: mp
    name: str

    def __repr__(self) -> str:
        return f"{self.dt}\t{self.mp.point}\t{self.name} progression at\t{self.mp.tropical.position}"

    def label(self) -> str:
        return f"{self.mp.point} {self.name} progression at {self.mp.tropical.position}"
