from dataclasses import dataclass
from datetime import datetime
import multiprocessing
from objects.points import get_default_angle_targets
from core.position import Position as pp
from util.interval import calculate_intervals
from typing import List, Dict


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


def get_all_angles_in_date_range(planet: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    targets = get_default_angle_targets(planet)
    return [angle for target in targets for angle in get_angles(planet, target, start, end, interval)]


def get_all_angles(planet: str, dt: datetime) -> Dict[str, List[Angle]]:
    targets = get_default_angle_targets(planet)
    angles_dict = {}
    angles_dict[planet] = []
    for target in targets:
        angles_dict[planet].append(get_angle(planet, target, dt))
    return angles_dict


def get_angles(planet1: str, planet2: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    datetimes = calculate_intervals(start, end, interval)

    return [get_angle(planet1, planet2, t) for t in datetimes]


def get_angle(planet1: str, planet2: str, dt: datetime) -> Angle:
    pos1 = pp.from_datetime(planet1, dt)
    pos2 = pp.from_datetime(planet2, dt)

    return Angle(dt, pos1, pos2)
