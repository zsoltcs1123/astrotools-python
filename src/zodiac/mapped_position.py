from datetime import datetime, timedelta
from typing import List
from core.base_position import BasePosition
from dataclasses import dataclass
from core.position_factory import create_position
from objects.points import ASC, MC
from zodiac.tropical_attributes import TropicalAttributes
from zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedPosition:
    def __init__(self, base_position: BasePosition):
        self.base_position = base_position
        self.retrograde = self.base_position.speed.decimal < 0
        self.stationary = self.base_position.speed.decimal == 0
        self.direction = "R" if self.retrograde else "S" if self.stationary else "D"
        self._tropical_attributes = None
        self._vedic_attributes = None
        self.previous_bps = {}

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[BasePosition]):
        return [cls(position) for position in planetary_positions]

    @property
    def dt(self) -> datetime:
        return self.base_position.dt

    @property
    def point(self) -> str:
        return self.base_position.point

    @property
    def tropical(self) -> TropicalAttributes:
        if self._tropical_attributes is None:
            self._tropical_attributes = TropicalAttributes(self.base_position)
        return self._tropical_attributes

    @property
    def vedic(self) -> VedicAttributes:
        if self._vedic_attributes is None:
            self._vedic_attributes = VedicAttributes(self.base_position)
        return self._vedic_attributes

    @property
    def daily_speed_index(self) -> str:
        pbp = self._get_previous_base_position()

        if pbp is None:
            return ""

        diff = round(self.base_position.speed.decimal - pbp.speed.decimal, 4)

        if diff == 0:
            return "="
        elif self.base_position.speed.decimal > pbp.speed.decimal:
            return "+"
        elif self.base_position.speed.decimal < pbp.speed.decimal:
            return "-"

    @property
    def daily_declination_index(self) -> str:
        bp = self._get_previous_base_position()

        if bp is None:
            return ""

        diff = round(self.base_position.dec.decimal - bp.dec.decimal, 4)

        if diff == 0:
            return "="
        elif self.base_position.dec.decimal > bp.dec.decimal:
            return "+"
        elif self.base_position.dec.decimal < bp.dec.decimal:
            return "-"

    def _get_previous_base_position(self, minutes=1440) -> BasePosition:
        if self.base_position.point in [ASC, MC]:
            return None

        return self.previous_bps.get(self.point, None) or create_position(
            self.point, self.dt - timedelta(minutes=minutes)
        )
