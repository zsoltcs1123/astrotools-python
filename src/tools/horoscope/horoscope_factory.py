from datetime import datetime
from typing import Dict, List
from core.angle import Angle
from core.enums import HoroscopeType, HouseSystem
from core.position_factory import create_position
from events.aspect_finder import AspectFinder
from objects.orb_map import OrbMap
from objects.points import (
    ASC,
    MC,
    get_default_angle_targets,
)
from tools.horoscope.horoscope import Horoscope
from tools.horoscope.horoscope_config import HoroscopeConfig
from tools.horoscope.vedic_horoscope import VedicHoroscope
from util.interval import calculate_intervals
from core.geo_position import GeoPosition as bp
from zodiac.mapped_position import MappedPosition as mp
import core.swisseph_api as swe_api


def create_horoscopes(
    start: datetime, end: datetime, interval_minutes: int, config: HoroscopeConfig
) -> List[Horoscope]:
    dts = calculate_intervals(start, end, interval_minutes)

    return [create_horoscope(dt, config) for dt in dts]


def create_horoscope(dt: datetime, config: HoroscopeConfig) -> Horoscope:
    aspect_finder = _create_asp_finder(config)
    cusps, ascmc = (
        _calculate_cusps_ascmc(dt, config) if ASC or MC in config.points else ([], [])
    )

    mps = _generate_positions(dt, config, ascmc)
    angles = _generate_angles(mps)
    aspects = _generate_aspects(aspect_finder, angles)

    if config.type == HoroscopeType.TROPICAL:
        return Horoscope(dt, config, mps, angles, aspects, cusps)
    else:
        mp_asc = next(mp for mp in mps if mp.point == ASC)
        cusps = _transform_cusps(dt, config, cusps, mp_asc.vedic.lon.decimal)
        return VedicHoroscope(dt, config, mps, angles, aspects, cusps)


def _transform_cusps(
    dt: datetime, config: HoroscopeConfig, cusps: List[float], sid_asc: float
):
    ayanamsa = swe_api.get_ayanamsha(dt.year, dt.month, "LAHIRI")

    if config.house_system == HouseSystem.PLACIDUS:
        return [(c - ayanamsa) % 360 for c in cusps]
    elif config.house_system == HouseSystem.WHOLE_SIGN:
        asc_sign_start = int(sid_asc / 30) * 30
        return [(asc_sign_start + i * 30) % 360 for i in range(12)]


def _create_asp_finder(config: HoroscopeConfig) -> AspectFinder:
    aspect_finder = None

    if config.aspects:
        orb_map = config.orb_map if config.orb_map else OrbMap.default()
        aspect_finder = AspectFinder(orb_map, config.aspects)

    return aspect_finder


def _generate_positions(
    dt: datetime,
    config: HoroscopeConfig,
    ascmc: tuple,
) -> List[mp]:
    mps = []
    for point in config.points:
        pos = None
        if point == ASC:
            pos = bp(dt, ASC, ascmc[0], 0, 0, 0, 0)
        elif point == MC:
            pos = bp(dt, MC, ascmc[1], 0, 0, 0, 0)
        else:
            pos = create_position(point, dt)

        mps.append(mp(pos))
    return mps


def _calculate_cusps_ascmc(dt: datetime, config: HoroscopeConfig) -> tuple:
    return swe_api.get_tropical_houses_and_ascmc(
        dt, config.lat, config.lon, config.house_system
    )


def _generate_angles(mps: List[mp]) -> Dict[str, List[Angle]]:
    angles = {}
    for mp in mps:
        targets = get_default_angle_targets(mp.point)
        angles[mp.point] = []

        for t in targets:
            target_mp = next((p for p in mps if p.point == t), None)
            if target_mp != None:
                angle = Angle(mp, target_mp)
                angles[mp.point].append(angle)

    return angles


def _generate_aspects(aspect_finder: AspectFinder, angles: Dict[str, List[Angle]]):
    if aspect_finder is None:
        return []

    return aspect_finder.find_aspects(angles)
