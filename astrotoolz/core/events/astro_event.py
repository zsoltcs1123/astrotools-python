from dataclasses import dataclass
from datetime import datetime

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.positions.base_position import BasePosition


@dataclass
class AstroEvent:
    dt: datetime  # UTC
    type: str
    coord_system: CoordinateSystem

    def tv_timestamp(self) -> str:
        """eg. timestamp("2023-02-27 11:05 UTC")"""
        return f'timestamp("{self.dt.strftime("%Y-%m-%d %H:%M UTC")}")'


@dataclass
class PositionalEvent(AstroEvent):
    current: BasePosition

    def __init__(self, type: str, current: BasePosition):
        super().__init__(current.dt, type, current.coord_system)
        self.current = current


@dataclass
class PositionChangeEvent(PositionalEvent):
    previous: BasePosition

    def __init__(
        self,
        type: str,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(type, current)
        self.previous = previous


@dataclass
class TropicalEvent(PositionChangeEvent):

    def __init__(
        self,
        type: str,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(type, current, previous)


@dataclass
class SiderealEvent(PositionChangeEvent):

    def __init__(
        self,
        type: str,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(type, current, previous)


@dataclass
class TropicalSignChange(TropicalEvent):

    def __init__(
        self,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(TropicalSignChange.__name__, current, previous)


@dataclass
class SiderealSignChange(SiderealEvent):

    def __init__(
        self,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(SiderealSignChange.__name__, current, previous)


@dataclass
class DecanChange(TropicalEvent):

    def __init__(
        self,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(DecanChange.__name__, current, previous)


@dataclass
class TermChange(TropicalEvent):

    def __init__(
        self,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(TermChange.__name__, current, previous)


@dataclass
class NakshatraChange(SiderealEvent):

    def __init__(
        self,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(NakshatraChange.__name__, current, previous)


@dataclass
class DirectionChange(PositionChangeEvent):

    def __init__(
        self,
        type: str,
        current: BasePosition,
        previous: BasePosition,
    ):
        super().__init__(type, current, previous)


@dataclass
class ExtremeEvent(PositionalEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)


@dataclass
class DeclinationExtreme(ExtremeEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)


@dataclass
class LatitudeExtreme(ExtremeEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)


@dataclass
class SpeedExtreme(ExtremeEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)


@dataclass
class PhaseExtreme(ExtremeEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)


@dataclass
class TropicalProgression(PositionalEvent):

    def __init__(self, type: str, current: BasePosition):
        super().__init__(type, current)
