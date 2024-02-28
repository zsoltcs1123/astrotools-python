from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from astrotoolz.core.units.degree import Degree


@dataclass
class BasePosition:
    dt: datetime
    point: str
    lon: Degree
    lat: Degree
    speed: Degree
    ra: Optional[Degree]
    dec: Optional[Degree]
