from typing import List
from datetime import datetime as dt, timezone
from core.base_position import BasePosition
from objects.points import NN, PLANETS, SN
from util.interval import calculate_intervals
import core.swisseph_api as swe_api


class PositionFactory:
    def __init__(self, node_calc: str):
        self.node_calc = node_calc

    def _planet(self, planet_name: str, dt: dt) -> BasePosition:
        lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
        ra, dec = swe_api.get_equatorial_position(planet_name, dt)
        return BasePosition(dt, planet_name, lon, lat, speed, ra, dec)

    def _north_node(self, dt: dt) -> BasePosition:
        pos = self._planet(self.node_calc, dt)
        pos.point = NN
        return pos

    def _south_node(self, dt: dt) -> BasePosition:
        nn = self._north_node(dt)
        lon = (nn.lon.dec + 180.0) % 360
        lat = 0
        speed = -nn.speed.dec
        ra = (nn.ra.dec + 12.0) % 24.0
        dec = -nn.dec.dec
        return BasePosition(dt, SN, lon, lat, speed, ra, dec)

    def create_position(self, point: str, dt: dt) -> BasePosition:
        dt = dt.replace(tzinfo=timezone.utc)
        if point in PLANETS:
            return self._planet(point, dt)
        elif point == NN:
            return self._north_node(dt)
        elif point == SN:
            return self._south_node(dt)
        else:
            raise (ValueError(f"{point} not supported"))

    def create_positions(
        self, point: str, start: dt, end: dt, interval_minutes: int
    ) -> List[BasePosition]:
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]
