from dataclasses import dataclass
from datetime import datetime

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedPosition:
    coord_system: CoordinateSystem
    dt: datetime
    point: str
    tropical: TropicalAttributes
    vedic: VedicAttributes

    def __init__(
        self,
        base_position: BasePosition,
        tropical_attributes: TropicalAttributes,
        vedic_attributes: VedicAttributes,
    ):
        self.base_position = base_position
        self.tropical = tropical_attributes
        self.vedic = vedic_attributes
        self.dt = self.base_position.dt
        self.point = self.base_position.point
