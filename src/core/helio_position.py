from dataclasses import dataclass
from datetime import datetime
from core.base_position import BasePosition
from core.degree import Degree


@dataclass
class HelioPosition(BasePosition):
    def __init__(self, dt: datetime, point: str, lon: float, lat: float, speed: float):
        self.dt = dt
        self.point = point
        self.lon = Degree.from_decimal(lon)
        self.lat = Degree.from_decimal(lat)
        self.speed = Degree.from_decimal(speed)
