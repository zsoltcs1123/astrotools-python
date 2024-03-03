from dataclasses import dataclass
from typing import Optional

from astrotoolz.core.points import ANGULARS
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedPosition(BasePosition):
    direction: str
    tropical: TropicalAttributes
    vedic: VedicAttributes

    def __init__(
        self,
        base_position: BasePosition,
        tropical_attributes: Optional[TropicalAttributes],
        vedic_attributes: Optional[VedicAttributes],
    ):
        self.dt = base_position.dt
        self.coord_system = base_position.coord_system
        self.point = base_position.point
        self.lon = base_position.lon
        self.lat = base_position.lat
        self.speed = base_position.speed
        self.ra = base_position.ra
        self.dec = base_position.dec

        self.tropical = tropical_attributes
        self.vedic = vedic_attributes
        self.direction = (
            "D"
            if self.point in ANGULARS
            else (
                "R"
                if self.speed.decimal < 0
                else "S" if self.speed.decimal == 0 else "D"
            )
        )
