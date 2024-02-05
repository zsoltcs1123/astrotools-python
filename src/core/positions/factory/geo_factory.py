from datetime import datetime
from typing import List

import core.ephemeris.swisseph_api as swe_api
from core.enums import NodeCalc
from core.objects.points import NN, PLANETS, SN
from core.positions.geo_position import GeoPosition
from pytz import timezone
from util.common import _to_degree
from util.interval import calculate_intervals


class GeoFactory:
    node_calc: NodeCalc

    def __init__(self, node_calc: NodeCalc):
        self.node_calc = node_calc

    def create_positions(
        self, point: str, start: datetime, end: datetime, interval_minutes: int
    ) -> List[GeoPosition]:
        self._logger.debug(
            f"Generating positions for config: {point}, {start}, {end}, {interval_minutes}"
        )
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]

    def create_position(self, point: str, dt: datetime) -> GeoPosition:
        dt = dt.replace(tzinfo=timezone.utc)
        if point in PLANETS:
            return self._geo(point, dt)
        elif point == NN:
            return self._north_node(dt, self.node_calc)
        elif point == SN:
            return self._south_node(dt, self.node_calc)
        else:
            raise (ValueError(f"{point} not supported"))

    def _geo(self, planet_name: str, dt: datetime) -> GeoPosition:
        lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
        ra, dec = swe_api.get_equatorial_position(planet_name, dt)
        lon, lat, speed, ra, dec = _to_degree(lon, lat, speed, ra, dec)
        return GeoPosition(dt, planet_name, lon, lat, speed, ra, dec)

    def _north_node(self, dt: datetime) -> GeoPosition:
        pos = self._geo(self.node_calc.swe_flag(), dt)
        pos.point = NN
        return pos

    def _south_node(self, dt: datetime, node_calc: NodeCalc) -> GeoPosition:
        nn = self._north_node(dt, node_calc.swe_flag())
        lon = (nn.lon.decimal + 180.0) % 360
        lat = 0
        speed = nn.speed.decimal
        ra = (nn.ra.decimal + 12.0) % 24.0
        dec = -nn.dec.decimal
        lon, lat, speed, ra, dec = _to_degree(lon, lat, speed)
        return GeoPosition(dt, SN, lon, lat, speed, ra, dec)
