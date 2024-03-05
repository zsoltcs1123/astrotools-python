from dataclasses import dataclass
from typing import List, Optional

from astrotoolz.core.enums import HouseSystem, Zodiac
from astrotoolz.core.events.orb_calculator import DynamicOrbCalculator
from astrotoolz.core.points import (
    ALL_POINTS,
    ANGULARS,
    MEAN_NODE,
    VEDIC_POINTS,
)
from astrotoolz.timeline.aspect_config import AspectsConfig


@dataclass
class HoroscopeConfig:
    name: str
    points: List[str]
    lat: Optional[float]
    lon: Optional[float]
    aspects: Optional[List[AspectsConfig]]
    zodiac: Optional[Zodiac]
    house_system: Optional[HouseSystem]

    def validate(self):

        angulars = True if any(point in ANGULARS for point in self.points) else False

        if angulars and (self.lat is None or self.lon is None):
            raise ValueError(
                "Latitude and longitude must be provided for angular points"
            )

        for p in self.points:
            if p not in ALL_POINTS:
                raise ValueError(f"{p} is not a valid point")

    @classmethod
    def default_tropical(cls, lat, lon, name):
        return cls(
            name,
            lat,
            lon,
            Zodiac.TROPICAL,
            ANGULARS + ALL_POINTS,
            MEAN_NODE,
            [AspectsConfig(30, True, DynamicOrbCalculator())],
            HouseSystem.PLACIDUS,
        )

    @classmethod
    def default_vedic(cls, lat, lon, name):
        return cls(
            name,
            lat,
            lon,
            Zodiac.SIDEREAL,
            ANGULARS + VEDIC_POINTS,
            MEAN_NODE,
            [AspectsConfig(30, True, DynamicOrbCalculator())],
            HouseSystem.WHOLE_SIGN,
        )
