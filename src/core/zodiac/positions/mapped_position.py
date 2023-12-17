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
    def __init__(
        self, root_position: RootPosition, previous_position: "MappedPosition" = None
    ):
        self.root_position = root_position
        self.previous_position = previous_position

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

    def get_root_attr_index(self, field_name: str) -> str:
        if self.previous_position is None:
            return ""

        self_value = getattr(self.root_position, field_name)
        prev_value = getattr(self.previous_position.root_position, field_name)

        if not isinstance(self_value, Degree) or not isinstance(prev_value, Degree):
            return ""

        return self._get_index(self_value, prev_value)

    def get_self_attr_index(self, field_name: str) -> str:
        if self.previous_position is None:
            return ""

        self_value = getattr(self, field_name)
        prev_value = getattr(self.previous_position, field_name)

        if not isinstance(self_value, Degree) or not isinstance(prev_value, Degree):
            return ""

        return self._get_index(self_value, prev_value)

    def _get_index(self, current_degree: Degree, previous_degree: Degree) -> str:
        if current_degree == previous_degree:
            return "="
        elif current_degree > previous_degree:
            return "+"
        elif current_degree < previous_degree:
            return "-"
