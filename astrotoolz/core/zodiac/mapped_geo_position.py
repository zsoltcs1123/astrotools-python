from dataclasses import dataclass

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.positions.geo_position import GeoPosition
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedGeoPosition(MappedPosition):
    base_position: GeoPosition
    retrograde: bool
    stationary: bool
    direction: str

    def __init__(
        self,
        base_position: GeoPosition,
        tropical_attributes: TropicalAttributes,
        vedic_attributes: VedicAttributes,
    ):
        super().__init__(base_position, tropical_attributes, vedic_attributes)
        self.coord_system = CoordinateSystem.GEO
        self.retrograde = self.base_position.speed.decimal < 0
        self.stationary = self.base_position.speed.decimal == 0
        self.direction = "R" if self.retrograde else "S" if self.stationary else "D"
