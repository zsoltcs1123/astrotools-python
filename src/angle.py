from dataclasses import dataclass
from datetime import datetime
import multiprocessing
from longitude import planet_longitude
from planet import get_angle_targets
from position import Position
from timegen import calculate_intervals
from typing import List


@dataclass
class Angle:
    time: datetime
    pos1: Position
    pos2: Position
    diff: float

    def __hash__(self) -> int:
        return hash((self.time, self.pos1, self.pos2, self.diff))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Angle):
            return False
        return self.time == other.time and self.pos1 == other.pos1 and self.pos2 == other.pos2 and self.diff == other.diff

    def __repr__(self) -> str:
        return f"{self.time}, {self.pos1}, {self.pos2}, {self.diff:.3f}"


def get_all_angles_multi(planet: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    targets = get_angle_targets(planet)
    return [angle for target in targets for angle in get_angles_multi(planet, target, start, end, interval)]


def get_angles(planet1: str, planet2: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    datetimes = calculate_intervals(start, end, interval)

    return [get_angle(planet1, planet2, t) for t in datetimes]


def get_angles_multi(planet1: str, planet2: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
    datetimes = calculate_intervals(start, end, interval)

    args = [(planet1, planet2, t) for t in datetimes]

    with multiprocessing.Pool() as pool:
        return pool.starmap(get_angle, args)


def get_angle(planet1: str, planet2: str, dt: datetime) -> Angle:
    lon1 = planet_longitude(planet1, dt).degrees
    lon2 = planet_longitude(planet2, dt).degrees

    pos1 = Position(dt, planet1, lon1)
    pos2 = Position(dt, planet2, lon2)

    return Angle(dt, pos1, pos2, diff(lon1, lon2))


def diff(lon1: float, lon2: float) -> float:
    return (lon1 - lon2) % 360
