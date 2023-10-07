from dataclasses import dataclass
from datetime import datetime as dt
from timegen.interval import calculate_intervals
import core.swisseph_api as swe_api


@dataclass
class PlanetaryPosition:
    dt: dt
    planet: str
    lon: float
    lat: float
    speed: float
    dec: float
    ra: float

    @classmethod
    def from_datetime(cls, planet: str, dt: dt):
        lon, lat, speed = swe_api.get_ecliptic_position(planet, dt)
        ra, dec = swe_api.get_equatorial_position(planet, dt)
        return cls(dt, planet, lon, lat, speed, dec, ra)

    @classmethod
    def from_datetime_range(cls, planet: str, start: dt, end: dt, interval_minutes: int):
        dts = calculate_intervals(start, end, interval_minutes)
        return [cls.from_datetime(planet, dt) for dt in dts]

    def __repr__(self):
        return f"Planet: {self.planet}\nDatetime: {self.dt.strftime('%Y-%m-%d %H:%M:%S')}\nLongitude: {self.lon:.2f}°\nLatitude: {self.lat:.2f}°\nRight Ascension: {self.ra:.2f}°\nDeclination: {self.dec:.2f}°\nSpeed: {self.speed:.2f}°/day"
