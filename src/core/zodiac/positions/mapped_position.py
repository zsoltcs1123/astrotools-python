from dataclasses import dataclass
from datetime import datetime
from typing import List
from core.positions.root_position import RootPosition
from core.units.degree import Degree
from util.cached_property import CachedProperty
from core.zodiac.attributes.tropical_attributes import TropicalAttributes
from core.zodiac.attributes.vedic_attributes import VedicAttributes


@dataclass
class MappedPosition:
    def __init__(self, root_position: RootPosition):
        self.root_position = root_position

    @classmethod
    def from_planetary_positions(cls, planetary_positions: List[RootPosition]):
        return [cls(position) for position in planetary_positions]

    @property
    def dt(self) -> datetime:
        return self.root_position.dt

    @property
    def point(self) -> str:
        return self.root_position.point

    @CachedProperty
    def tropical(self) -> TropicalAttributes:
        return TropicalAttributes(self.root_position)

    @CachedProperty
    def vedic(self) -> VedicAttributes:
        return VedicAttributes(self.root_position)
