from datetime import datetime
from dataclasses import dataclass
from typing import List
from timegen.interval import calculate_intervals
from core.skyfield_api import get_tropical_longitude, get_declination


@dataclass
class PlanetaryPosition:
    time: datetime
    planet: str
    lon: float
    dec: float

    def __hash__(self):
        return hash((self.time, self.planet, self.lon, self.dec))

    def __eq__(self, other):
        if not isinstance(other, PlanetaryPosition):
            return False
        return self.time == other.time and self.planet == other.planet and self.lon == other.lon and self.dec == other.dec

    def __repr__(self):
        return f"[{self.planet}, {self.lon:.3f}, {self.dec:.3f}]"


def get_planetary_position(planet_name:str, date: datetime) -> PlanetaryPosition:
    lon = get_tropical_longitude(planet_name, date)
    dec = get_declination(planet_name, date)
    return PlanetaryPosition(date, planet_name, lon.degrees, dec.degrees)


def get_planetary_positions(planet_name:str, start_time: datetime, end_time: datetime, interval_minutes: int) -> List[PlanetaryPosition]:
    return [get_planetary_position(planet_name, time) for time in calculate_intervals(start_time, end_time, interval_minutes)]



