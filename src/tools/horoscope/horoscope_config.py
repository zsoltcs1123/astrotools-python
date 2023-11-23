
from typing import List
from dataclasses import dataclass
from datetime import datetime

from core.enums import AspectType, CoordinateSystem, HouseSystem
from events.aspect import DEFAULT_ASPECTS
from objects.points import ALL_POINTS, ASC, MC, MEAN_NODE


@dataclass
class HoroscopeConfig:
    lat: float
    lon: float
    name: str
    points: List[str]
    aspects: List[AspectType]
    house_system: HouseSystem
    coord_system: CoordinateSystem
    node_calc: str


    @classmethod
    def default(
        cls,
        lat,
        lon,
        name
    ):
        return cls(
            lat,
            lon,
            name,
            ALL_POINTS + [ASC, MC],
            DEFAULT_ASPECTS,
            HouseSystem.PLACIDUS,
            CoordinateSystem.GEO,
            MEAN_NODE
        )
