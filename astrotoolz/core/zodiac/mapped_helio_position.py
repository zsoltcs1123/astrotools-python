from dataclasses import dataclass

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.tropical_attributes import TropicalAttributes
from astrotoolz.core.zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedHelioPosition(MappedPosition):
    def __init__(
        self,
        base_position: BasePosition,
        tropical_attributes: TropicalAttributes,
        vedic_attributes: VedicAttributes,
    ):
        super().__init__(base_position, tropical_attributes, vedic_attributes)
        self.coord_system = CoordinateSystem.HELIO
