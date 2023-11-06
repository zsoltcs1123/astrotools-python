from dataclasses import dataclass
from datetime import datetime
from core.position import Position as pp


@dataclass
class Angle:
    dt: datetime
    source: pp
    target: pp

    def __init__(self, source: pp, target: pp):
        self.source = source
        self.target = target
        self.dt = source.dt

    @property
    def diff(self):
        return abs(self.source.lon - self.target.lon)

    def __repr__(self) -> str:
        return f"{self.dt}: {self.source.name} [{self.source.lon:.3f}], {self.target.name} [{self.target.lon:.3f}], {self.diff:.3f}"

    def print_no_time(self):
        return f"{self.source.name} [{self.source.lon:.3f}], {self.target.name} [{self.target.lon:.3f}], {self.diff:.3f}"

