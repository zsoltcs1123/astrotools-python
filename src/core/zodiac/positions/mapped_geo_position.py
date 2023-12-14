from datetime import timedelta
from typing import List
from core.positions.geo_position import GeoPosition
from dataclasses import dataclass
from core.units.degree import Degree
from core.positions.root_position_factory import create_geo_position
from core.objects.points import ASC, MC, SUN
from util.cached_property import CachedProperty
from core.zodiac.positions.mapped_position import MappedPosition


@dataclass
class MappedGeoPosition(MappedPosition):
    def __init__(self, root_position: GeoPosition):
        self.base_position = root_position
        self.retrograde = self.base_position.speed.decimal < 0
        self.stationary = self.base_position.speed.decimal == 0
        self.direction = "R" if self.retrograde else "S" if self.stationary else "D"
        self._tropical_attributes = None
        self._vedic_attributes = None
        self.previous_bps = {}

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[GeoPosition]):
        return [cls(position) for position in planetary_positions]

    @CachedProperty
    def phase(self) -> Degree:
        from core.angles.angle import Angle

        sun = MappedGeoPosition(create_geo_position(SUN, self.dt))
        return Degree.from_decimal(Angle(self, sun).circular_diff)

    @property
    def daily_speed_index(self) -> str:
        pbp = self._get_previous_base_position()

        if pbp is None:
            return ""

        return self._get_index(self.base_position.speed.decimal, pbp.speed.decimal)

    @property
    def daily_declination_index(self) -> str:
        pbp = self._get_previous_base_position()

        if pbp is None:
            return ""

        return self._get_index(self.base_position.dec.decimal, pbp.dec.decimal)

    @property
    def phase_index(self) -> str:
        pbp = self._get_previous_base_position()

        if pbp is None:
            return ""

        pmp = MappedGeoPosition(pbp)
        return self._get_index(self.phase.decimal, pmp.phase.decimal)

    @property
    def daily_latitude_index(self) -> str:
        pbp = self._get_previous_base_position()

        if pbp is None:
            return ""

        return self._get_index(self.base_position.lat.decimal, pbp.lat.decimal)

    def _get_index(self, current_value: float, previous_value: float) -> str:
        diff = round(current_value - previous_value, 4)

        if diff == 0:
            return "="
        elif current_value > previous_value:
            return "+"
        elif current_value < previous_value:
            return "-"

    def _get_previous_base_position(self, minutes=1440) -> GeoPosition:
        if self.base_position.point in [ASC, MC]:
            return None

        return self.previous_bps.get(self.point, None) or create_geo_position(
            self.point, self.dt - timedelta(minutes=minutes)
        )
