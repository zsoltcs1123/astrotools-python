from dataclasses import dataclass
from core.enums import CoordinateSystem
from core.positions.base_position import BasePosition

from core.zodiac.positions.mapped_position import MappedPosition


@dataclass
class MappedHelioPosition(MappedPosition):
    def __init__(self, base_position: BasePosition):
        super().__init__(base_position)
        self.cs = CoordinateSystem.HELIO