from dataclasses import dataclass
from datetime import datetime
import multiprocessing
from core.skyfield_api import get_tropical_longitude
from core.planet import get_outer_planets_map
from core.planetary_position import PlanetaryPosition as pp
from timegen.interval import calculate_intervals
from typing import List


@dataclass
class Angle:
    time: datetime
    pos1: pp
    pos2: pp

    @property
    def diff(self):
        return abs(self.pos1.lon - self.pos2.lon)

    def __hash__(self) -> int:
        return hash((self.time, self.pos1, self.pos2, self.diff))

    def __eq__(self, other: 'Angle') -> bool:
        if not isinstance(other, Angle):
            return False
        return self.time == other.time and self.pos1 == other.pos1 and self.pos2 == other.pos2 and self.diff == other.diff

    def __repr__(self) -> str:
        return f"{self.time}: {self.pos1.planet} [{self.pos1.lon:.3f}], {self.pos2.planet} [{self.pos2.lon:.3f}], {self.diff:.3f}"


def get_all_angles_multiproc(planet: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    targets = get_outer_planets_map(planet)
    return [angle for target in targets for angle in get_angles_multiproc(planet, target, start, end, interval)]


def get_all_angles(planet: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    targets = get_outer_planets_map(planet)
    return [angle for target in targets for angle in get_angles(planet, target, start, end, interval)]


def get_angles(planet1: str, planet2: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    datetimes = calculate_intervals(start, end, interval)

    return [get_angle(planet1, planet2, t) for t in datetimes]


def get_angles_multiproc(planet1: str, planet2: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    datetimes = calculate_intervals(start, end, interval)

    args = [(planet1, planet2, t) for t in datetimes]

    with multiprocessing.Pool() as pool:
        return pool.starmap(get_angle, args)


def get_angle(planet1: str, planet2: str, dt: datetime) -> Angle:
    pos1 = pp.from_datetime(planet1, dt)
    pos2 = pp.from_datetime(planet2, dt)

    return Angle(dt, pos1, pos2)
