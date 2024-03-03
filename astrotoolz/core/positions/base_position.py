from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.units.degree import Degree


@dataclass
class BasePosition:
    dt: datetime
    coord_system: CoordinateSystem
    point: str
    lon: Degree
    lat: Degree
    speed: Degree
    ra: Optional[Degree]
    dec: Optional[Degree]
