from typing import List
from datetime import datetime as dt, timezone
from core.positions.position_factory_config import PositionFactoryConfig
from core.positions.base_position import BasePosition
from core.positions.geo_position import GeoPosition
from core.positions.helio_position import HelioPosition
from core.enums import CoordinateSystem, NodeCalc
from core.objects.points import EARTH, MEAN_NODE, MOON, NN, PLANETS, SN, SUN
from core.units.degree import Degree
from util.interval import calculate_intervals
import core.ephemeris.swisseph_api as swe_api


def create_position(point: str, dt: dt, coord_system: CoordinateSystem) -> BasePosition:
    return (
        create_geo_position(point, dt)
        if coord_system == CoordinateSystem.GEO
        else create_helio_position(point, dt)
    )


def create_geo_position(point: str, dt: dt, node_calc: str = MEAN_NODE) -> GeoPosition:
    dt = dt.replace(tzinfo=timezone.utc)
    if point in PLANETS:
        return _geo(point, dt)
    elif point == NN:
        return _north_node(dt, node_calc)
    elif point == SN:
        return _south_node(dt, node_calc)
    else:
        raise (ValueError(f"{point} not supported"))


def create_helio_position(point: str, dt: dt) -> HelioPosition:
    if point == SUN:
        raise (ValueError(f"{point} not supported"))
    if point in [MOON, SN, NN]:
        return _helio(EARTH, dt)
    else:
        return _helio(point, dt)


def create_helio_positions(config: PositionFactoryConfig) -> List[HelioPosition]:
    dts = calculate_intervals(config.start, config.end, config.interval_minutes)
    return [
        create_helio_position(config.point, dt, config.coordinate_system) for dt in dts
    ]


def create_geo_positions(config: PositionFactoryConfig) -> List[GeoPosition]:
    dts = calculate_intervals(config.start, config.end, config.interval_minutes)
    return [create_geo_position(config.point, dt, config.node_calc) for dt in dts]


def _helio(point: str, dt: dt) -> HelioPosition:
    lon, lat, speed = swe_api.get_helio_position(point, dt)
    lon, lat, speed = _to_degree(lon, lat, speed)
    return HelioPosition(dt, point, lon, lat, speed)


def _geo(planet_name: str, dt: dt) -> GeoPosition:
    lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
    ra, dec = swe_api.get_equatorial_position(planet_name, dt)
    lon, lat, speed, ra, dec = _to_degree(lon, lat, speed, ra, dec)
    return GeoPosition(dt, planet_name, lon, lat, speed, ra, dec)


def _north_node(dt: dt, node_calc: NodeCalc) -> GeoPosition:
    pos = _geo(node_calc.swe_flag(), dt)
    pos.point = NN
    return pos


def _south_node(dt: dt, node_calc: NodeCalc) -> GeoPosition:
    nn = _north_node(dt, node_calc.swe_flag())
    lon = (nn.lon.decimal + 180.0) % 360
    lat = 0
    speed = nn.speed.decimal
    ra = (nn.ra.decimal + 12.0) % 24.0
    dec = -nn.dec.decimal
    lon, lat, speed, ra, dec = _to_degree(lon, lat, speed)
    return GeoPosition(dt, SN, lon, lat, speed, ra, dec)


def _to_degree(*args: float) -> List[Degree]:
    return [Degree.from_decimal(arg) for arg in args]
