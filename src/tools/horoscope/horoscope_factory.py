from datetime import datetime, timedelta
from typing import Dict, List
from core.angles.angle import Angle
from core.angles.angle_factory import generate_angles_dict
from core.enums import HoroscopeType, HouseSystem
from core.positions.root_position_factory import create_geo_position
from events.aspects.aspect_finder import AspectFinder
from events.aspects.orb_map import OrbMap
from core.objects.points import (
    ASC,
    MC,
    SUN,
    get_default_angle_targets,
)
from tools.horoscope.horoscope import Horoscope
from tools.horoscope.horoscope_config import HoroscopeConfig
from tools.horoscope.vedic_horoscope import VedicHoroscope
from util.interval import calculate_intervals
from core.positions.geo_position import GeoPosition as gp
from core.zodiac.positions.mapped_geo_position import MappedGeoPosition as mgp
import core.ephemeris.swisseph_api as swe_api


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
    mps = _add_sun_position(mps)
    angles = generate_angles_dict(mps, get_default_angle_targets)
    aspects = _generate_aspects(aspect_finder, angles)

    if config.type == HoroscopeType.TROPICAL:
        return Horoscope(dt, config, mps, angles, aspects, cusps)
    else:
        mp_asc = next(mp for mp in mps if mp.point == ASC)
        cusps = _transform_cusps(dt, config, cusps, mp_asc.vedic.lon.decimal)
        return VedicHoroscope(dt, config, mps, angles, aspects, cusps)


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
) -> List[mgp]:
    mps = []
    for point in config.points:
        gp = _create_gp(point, dt, ascmc)
        prev_dt = dt - timedelta(hours=24)
        prev_gp = _create_gp(point, prev_dt, ascmc)
        mps.append(mgp(gp, mgp(prev_gp)))
    return mps


def _create_gp(point: str, dt: datetime, ascmc: tuple) -> gp:
    if point == ASC:
        return gp(dt, ASC, ascmc[0], 0, 0, 0, 0)
    elif point == MC:
        return gp(dt, MC, ascmc[1], 0, 0, 0, 0)
    else:
        return create_geo_position(point, dt)


def _add_sun_position(mgps: List[mgp]) -> List[mgp]:
    sun = next(mgp for mgp in mgps if mgp.point == SUN)
    if sun is None:
        sun = create_geo_position(SUN, mgps[0].dt)

    for mgp in mgps:
        mgp.sun_position = sun
        mgp.previous_position.sun_position = sun

    return mgps


def _calculate_cusps_ascmc(dt: datetime, config: HoroscopeConfig) -> tuple:
    return swe_api.get_tropical_houses_and_ascmc(
        dt, config.lat, config.lon, config.house_system
    )


def _generate_aspects(aspect_finder: AspectFinder, angles: Dict[str, List[Angle]]):
    if aspect_finder is None:
        return []

    return aspect_finder.find_aspects(angles)


def _transform_cusps(
    dt: datetime, config: HoroscopeConfig, cusps: List[float], sid_asc: float
):
    ayanamsa = swe_api.get_ayanamsha(dt.year, dt.month, "LAHIRI")

    if config.house_system == HouseSystem.PLACIDUS:
        return [(c - ayanamsa) % 360 for c in cusps]
    elif config.house_system == HouseSystem.WHOLE_SIGN:
        asc_sign_start = int(sid_asc / 30) * 30
        return [(asc_sign_start + i * 30) % 360 for i in range(12)]
