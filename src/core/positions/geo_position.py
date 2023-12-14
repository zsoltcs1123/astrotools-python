from dataclasses import dataclass
from datetime import datetime as dt
from core.positions.root_position import RootPosition
from core.units.degree import Degree


@dataclass
class GeoPosition(RootPosition):
    ra: Degree
    dec: Degree

    def __init__(
        self,
        dt: dt,
        point: str,
        lon: float,
        lat: float,
        speed: float,
        ra: float,
        dec: float,
    ):
        self.dt = dt
        self.point = point
        self.lon = Degree.from_decimal(lon)
        self.lat = Degree.from_decimal(lat)
        self.speed = Degree.from_decimal(speed)
        self.ra = Degree.from_decimal(ra)
        self.dec = Degree.from_decimal(dec)

    def __repr__(self):
        return (
            f"Point: {self.point}\n"
            f"Datetime: {self.dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Longitude: {self.lon}\n"
            f"Latitude: {self.lat}\n"
            f"Right Ascension: {self.ra}\n"
            f"Declination: {self.dec}\n"
            f"Speed: {self.speed}"
        )
