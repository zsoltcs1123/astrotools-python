from dataclasses import dataclass
from datetime import datetime
import multiprocessing
from points.planets import get_outer_planets_map
from core.position import Position as pp
from util.interval import calculate_intervals
from typing import List, Dict


@dataclass
class Angle:
    time: datetime
    pos1: pp
    pos2: pp

    @property
    def diff(self):
        return abs(self.pos1.lon - self.pos2.lon)

    def __repr__(self) -> str:
        return f"{self.time}: {self.pos1.point} [{self.pos1.lon:.3f}], {self.pos2.point} [{self.pos2.lon:.3f}], {self.diff:.3f}"

    def print_no_time(self):
        return f"{self.pos1.point} [{self.pos1.lon:.3f}], {self.pos2.point} [{self.pos2.lon:.3f}], {self.diff:.3f}"


def get_all_angles_in_date_range(planet: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    targets = get_outer_planets_map(planet)
    return [angle for target in targets for angle in get_angles(planet, target, start, end, interval)]


def get_all_angles(planet: str, dt: datetime) -> Dict[str, List[Angle]]:
    targets = get_outer_planets_map(planet)
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
