from dataclasses import dataclass
from datetime import datetime
from core.base_position import BasePosition as bp


@dataclass
class Angle:
    dt: datetime
    source: bp
    target: bp

    def __init__(self, source: bp, target: bp):
        self.source = source
        self.target = target
        self.dt = source.dt

    @property
    def diff(self):
        return abs(self.source.lon.dec - self.target.lon.dec)

    def __repr__(self) -> str:
        return f"{self.dt}: {self.source.point} [{self.source.lon.dec:.3f}], {self.target.point} [{self.target.lon.dec:.3f}], {self.diff:.3f}"

    def print_no_time(self):
        return f"{self.source.point} [{self.source.lon.dec:.3f}], {self.target.point} [{self.target.lon.dec:.3f}], {self.diff:.3f}"
