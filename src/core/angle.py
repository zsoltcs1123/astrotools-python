from dataclasses import dataclass
from datetime import datetime
from zodiac.mapped_position import MappedPosition as mp


@dataclass
class Angle:
    dt: datetime
    source: mp
    target: mp

    def __init__(self, source: mp, target: mp):
        self.source = source
        self.target = target
        self.dt = source.dt

    @property
    def abs_diff(self):
        return abs(
            self.source.base_position.lon.decimal
            - self.target.base_position.lon.decimal
        )
