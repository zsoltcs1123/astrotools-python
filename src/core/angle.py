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
    def diff(self):
        return abs(
            self.source.base_position.lon.decimal
            - self.target.base_position.lon.decimal
        )

    def print_tropical_no_time(self):
        return f"{self.source.point} [{self.source.tropical.lon.decimal:.3f}], {self.target.point} [{self.target.tropical.lon.decimal:.3f}], {self.diff:.3f}"

    def print_vedic_no_time(self):
        return f"{self.source.point} [{self.source.vedic.lon.decimal:.3f}], {self.target.point} [{self.target.vedic.lon.decimal:.3f}], {self.diff:.3f}"
