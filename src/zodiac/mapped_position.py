from datetime import datetime
from core import base_position
from core.base_position import BasePosition
from dataclasses import dataclass
from zodiac.tropical_attributes import TropicalAttributes
from zodiac.vedic_attributes import VedicAttributes


@dataclass
class MappedPosition:
    def __init__(self, base_position: BasePosition):
        self.base_position = base_position
        self.retrograde = self.base_position.speed.dec < 0
        self.stationary = self.base_position.speed.dec == 0
        self.direction = "R" if self.retrograde else "S" if self.stationary else "D"
        self._tropical_attributes = None
        self._vedic_attributes = None

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
