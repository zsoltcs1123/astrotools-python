from dataclasses import dataclass
from datetime import datetime
from core.positions.root_position import RootPosition
from core.units.degree import Degree


@dataclass
class HelioPosition(RootPosition):
    def __init__(self, dt: datetime, point: str, lon: float, lat: float, speed: float):
        self.dt = dt
        self.point = point
        self.lon = Degree.from_decimal(lon)
        self.lat = Degree.from_decimal(lat)
        self.speed = Degree.from_decimal(speed)

    def __repr__(self):
        return (
            f"Point: {self.point}\n"
            f"Datetime: {self.dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Longitude: {self.lon}\n"
            f"Latitude: {self.lat}\n"
            f"Speed: {self.speed}"
        )
