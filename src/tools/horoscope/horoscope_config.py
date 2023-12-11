from typing import List
from dataclasses import dataclass
from core.enums import AspectType, CoordinateSystem, HoroscopeType, HouseSystem
from events.aspect import DEFAULT_ASPECTS
from objects.orb_map import OrbMap
from objects.points import ALL_POINTS, ANGULARS, MEAN_NODE, VEDIC_POINTS


@dataclass
class HoroscopeConfig:
    lat: float
    lon: float
    name: str
    type: HoroscopeType
    points: List[str]
    aspects: List[AspectType]
    orb_map: OrbMap
    house_system: HouseSystem
    coord_system: CoordinateSystem
    node_calc: str

    @classmethod
    def default_tropical_snapshot(cls, lat, lon, name):
        return cls(
            lat,
            lon,
            name,
            HoroscopeType.TROPICAL,
            ANGULARS + ALL_POINTS,
            DEFAULT_ASPECTS,
            OrbMap.default(),
            HouseSystem.PLACIDUS,
            CoordinateSystem.GEO,
            MEAN_NODE,
        )

    @classmethod
    def default_tropical_snapshot(cls, lat, lon, name):
        return cls(
            lat,
            lon,
            name,
            HoroscopeType.TROPICAL,
            ANGULARS + ALL_POINTS,
            DEFAULT_ASPECTS,
            OrbMap.from_float(2),
            HouseSystem.PLACIDUS,
            CoordinateSystem.GEO,
            MEAN_NODE,
        )

    @classmethod
    def default_vedic(cls, lat, lon, name):
        return cls(
            lat,
            lon,
            name,
            HoroscopeType.VEDIC,
            ANGULARS + VEDIC_POINTS,
            DEFAULT_ASPECTS,
            HouseSystem.WHOLE_SIGN,
            CoordinateSystem.GEO,
            MEAN_NODE,
        )
