from dataclasses import dataclass
from datetime import datetime

from astrotoolz.core.zodiac.mapped_position import MappedPosition


@dataclass
class Angle:
    dt: datetime
    source: MappedPosition
    target: MappedPosition

    def __init__(self, source: MappedPosition, target: MappedPosition):
        self.source = source
        self.target = target
        self.dt = source.dt
        self.abs_diff = self.calculate_abs_diff()
        self.real_diff = self.calculate_real_diff()
        self.circular_diff = self.calculate_circular_diff()

    def calculate_abs_diff(self) -> float:
        return abs(
            self.source.base_position.lon.decimal
            - self.target.base_position.lon.decimal
        )

    def calculate_real_diff(self) -> float:
        return (
            self.source.base_position.lon.decimal
            - self.target.base_position.lon.decimal
        )

    def calculate_circular_diff(self) -> float:
        diff = (
            self.source.base_position.lon.decimal
            - self.target.base_position.lon.decimal
        )
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360
        return diff
