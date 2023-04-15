from dataclasses import dataclass
import datetime
import multiprocessing
from longitude import planet_longitude
from position import Position
from timegen import calculate_intervals


@dataclass
class Angle:
    time: datetime
    pos1: Position
    pos2: Position
    diff: float

    def __hash__(self):
        return hash((self.time, self.pos1, self.pos2, self.diff))

    def __eq__(self, other):
        if not isinstance(other, Angle):
            return False
        return self.time == other.time and self.pos1 == other.pos1 and self.pos2 == other.pos2 and self.diff == other.diff

    def __repr__(self):
        return f"{self.time}, {self.pos1}, {self.pos2}, {self.diff:.3f})"


def get_angles(planet1, planet2, dt1, dt2, intervals):
    datetimes = calculate_intervals(dt1, dt2, intervals)

    return [get_angle(planet1, planet2, t) for t in datetimes]


def get_angles_multi(planet1, planet2, dt1, dt2, intervals):
    datetimes = calculate_intervals(dt1, dt2, intervals)

    args = [(planet1, planet2, t) for t in datetimes]

    with multiprocessing.Pool() as pool:
        return pool.starmap(get_angle, args)


def get_angle(planet1, planet2, t):
    lon1 = planet_longitude(planet1, t).degrees
    lon2 = planet_longitude(planet2, t).degrees

    pos1 = Position(t, planet1, lon1)
    pos2 = Position(t, planet2, lon2)

    return Angle(t, pos1, pos2, diff(lon1, lon2))


def diff(lon1, lon2):
    return (lon1 - lon2) % 360
