from typing import List, Optional
from core.positions.geo_position import GeoPosition
from dataclasses import dataclass
from core.units.degree import Degree
from util.cached_property import CachedProperty
from core.zodiac.positions.mapped_position import MappedPosition


@dataclass
class MappedGeoPosition(MappedPosition):
    root_position: GeoPosition
    retrograde: bool
    stationary: bool
    direction: str

    def __init__(
        self,
        root_position: GeoPosition,
        previous_position: "MappedGeoPosition" = None,
        sun_position: GeoPosition = None,
    ):
        self.root_position = root_position
        self.previous_position = previous_position
        self.sun_position = sun_position
        self.retrograde = self.root_position.speed.decimal < 0
        self.stationary = self.root_position.speed.decimal == 0
        self.direction = "R" if self.retrograde else "S" if self.stationary else "D"

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[GeoPosition]):
        return [cls(position) for position in planetary_positions]

    @CachedProperty
    def phase(self) -> Optional[Degree]:
        from core.angles.angle import Angle

        if self.sun_position is None:
            return None
        return Degree.from_decimal(Angle(self, self.sun_position).circular_diff)
