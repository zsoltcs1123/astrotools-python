from platform import node
from typing import List
from datetime import datetime as dt, timezone
from core.base_position import BasePosition
from objects.points import MEAN_NODE, NN, PLANETS, SN
from util.interval import calculate_intervals
import core.swisseph_api as swe_api


def create_positions(
    point: str,
    start: dt,
    end: dt,
    interval_minutes: int,
    node_calc: str = MEAN_NODE,
) -> List[BasePosition]:
    dts = calculate_intervals(start, end, interval_minutes)
    return [create_position(point, dt, node_calc) for dt in dts]


def create_position(point: str, dt: dt, node_calc: str = MEAN_NODE) -> BasePosition:
    dt = dt.replace(tzinfo=timezone.utc)
    if point in PLANETS:
        return _planet(point, dt)
    elif point == NN:
        return _north_node(dt, node_calc)
    elif point == SN:
        return _south_node(dt, node_calc)
    else:
        raise (ValueError(f"{point} not supported"))


def _planet(planet_name: str, dt: dt) -> BasePosition:
    lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
    ra, dec = swe_api.get_equatorial_position(planet_name, dt)
    return BasePosition(dt, planet_name, lon, lat, speed, ra, dec)


def _north_node(dt: dt, node_calc: str) -> BasePosition:
    pos = _planet(node_calc, dt)
    pos.point = NN
    return pos


def _south_node(dt: dt, node_calc: str) -> BasePosition:
    nn = _north_node(dt, node_calc)
    lon = (nn.lon.decimal + 180.0) % 360
    lat = 0
    speed = nn.speed.decimal
    ra = (nn.ra.decimal + 12.0) % 24.0
    dec = -nn.dec.decimal
    return BasePosition(dt, SN, lon, lat, speed, ra, dec)
