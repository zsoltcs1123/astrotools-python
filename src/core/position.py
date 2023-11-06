from dataclasses import dataclass
from datetime import datetime as dt
from objects.points import NN, PLANETS, SN
from util.interval import calculate_intervals
import core.swisseph_api as swe_api


@dataclass
class Position:
    dt: dt
    name: str
    lon: float
    lat: float
    speed: float
    ra: float
    dec: float

    def __repr__(self):
        return f"Point: {self.name}\nDatetime: {self.dt.strftime('%Y-%m-%d %H:%M:%S')}\nLongitude: {self.lon:.2f}°\nLatitude: {self.lat:.2f}°\nRight Ascension: {self.ra:.2f}°\nDeclination: {self.dec:.2f}°\nSpeed: {self.speed:.2f}°/day"
