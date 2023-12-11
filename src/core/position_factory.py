from platform import node
from typing import List
from datetime import datetime as dt, timezone
from core.geo_position import GeoPosition
from core.helio_position import HelioPosition
from objects.points import EARTH, MEAN_NODE, MOON, NN, PLANETS, SN, SUN
from util.interval import calculate_intervals
import core.swisseph_api as swe_api


def create_positions(
    point: str,
    start: dt,
    end: dt,
    interval_minutes: int,
    node_calc: str = MEAN_NODE,
) -> List[GeoPosition]:
    dts = calculate_intervals(start, end, interval_minutes)
    return [create_position(point, dt, node_calc) for dt in dts]


def create_position(point: str, dt: dt, node_calc: str = MEAN_NODE) -> GeoPosition:
    dt = dt.replace(tzinfo=timezone.utc)
    if point in PLANETS:
        return _planet(point, dt)
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


def _helio(point: str, dt: dt) -> HelioPosition:
    lon, lat, speed = swe_api.get_helio_position(point, dt)
    return HelioPosition(dt, point, lon, lat, speed)


def _planet(planet_name: str, dt: dt) -> GeoPosition:
    lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
    ra, dec = swe_api.get_equatorial_position(planet_name, dt)
    return GeoPosition(dt, planet_name, lon, lat, speed, ra, dec)


def _north_node(dt: dt, node_calc: str) -> GeoPosition:
    pos = _planet(node_calc, dt)
    pos.point = NN
    return pos


def _south_node(dt: dt, node_calc: str) -> GeoPosition:
    nn = _north_node(dt, node_calc)
    lon = (nn.lon.decimal + 180.0) % 360
    lat = 0
    speed = nn.speed.decimal
    ra = (nn.ra.decimal + 12.0) % 24.0
    dec = -nn.dec.decimal
    return GeoPosition(dt, SN, lon, lat, speed, ra, dec)
