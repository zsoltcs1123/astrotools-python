from dataclasses import dataclass
from datetime import datetime
from core.units.degree import Degree


@dataclass
class BasePosition:
    dt: datetime
    point: str
    lon: Degree
    lat: Degree
    speed: Degree
