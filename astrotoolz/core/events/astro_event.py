from dataclasses import dataclass
from datetime import datetime

from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.zodiac.mapped_position import MappedPosition


@dataclass
class AstroEvent:
    dt: datetime  # UTC
    type: str
    current: BasePosition

    def tv_timestamp(self) -> str:
        """eg. timestamp("2023-02-27 11:05 UTC")"""
        return f'timestamp("{self.dt.strftime("%Y-%m-%d %H:%M UTC")}")'


@dataclass
class PositionalEvent(AstroEvent):
    previous: MappedPosition


@dataclass
class TropicalEvent(PositionalEvent):
    pass


@dataclass
class SiderealEvent(PositionalEvent):
    pass


@dataclass
class TropicalSignChange(TropicalEvent):
    pass


@dataclass
class SiderealSignChange(SiderealEvent):
    pass


@dataclass
class DecanChange(TropicalEvent):
    pass


@dataclass
class TermChange(TropicalEvent):
    pass


@dataclass
class NakshatraChange(SiderealEvent):
    pass


@dataclass
class DirectionChange(PositionalEvent):
    pass


@dataclass
class ExtremeEvent(AstroEvent):
    pass


@dataclass
class DeclinationExtreme(ExtremeEvent):
    pass


@dataclass
class LatitudeExtreme(ExtremeEvent):
    pass


@dataclass
class SpeedExtreme(ExtremeEvent):
    pass


@dataclass
class PhaseExtreme(ExtremeEvent):
    pass


@dataclass
class TropicalProgression(AstroEvent):
    pass
