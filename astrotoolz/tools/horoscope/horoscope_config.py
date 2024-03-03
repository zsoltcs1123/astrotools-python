from dataclasses import dataclass
from typing import List, Optional

from astrotoolz.core.enums import (
    HouseSystem,
    NodeCalc,
    Zodiac,
)
from astrotoolz.core.points import ALL_POINTS, ANGULARS, MEAN_NODE, VEDIC_POINTS
from astrotoolz.timeline.aspect_config import AspectsConfig


@dataclass
class HoroscopeConfig:
    lat: float
    lon: float
    name: str
    zodiac: Zodiac
    points: List[str]
    node_calc: Optional[NodeCalc]
    aspects: Optional[List[AspectsConfig]]
    house_system: HouseSystem

    def validate(self):
        pass

    @classmethod
    def default_tropical(cls, lat, lon, name):
        return cls(
            lat,
            lon,
            name,
            Zodiac.TROPICAL,
            ANGULARS + ALL_POINTS,
            MEAN_NODE,
            [AspectsConfig(30, True)],
            HouseSystem.PLACIDUS,
        )

    @classmethod
    def default_vedic(cls, lat, lon, name):
        return cls(
            lat,
            lon,
            name,
            Zodiac.SIDEREAL,
            ANGULARS + VEDIC_POINTS,
            MEAN_NODE,
            [AspectsConfig(30, True)],
            HouseSystem.WHOLE_SIGN,
        )
