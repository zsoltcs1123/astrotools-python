from datetime import datetime

import pytz

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.core.points import NN, PLANETS, SN
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.util.common import to_degree


class GeoFactory(PositionFactory):
    node_calc: NodeCalc

    def __init__(self, node_calc: NodeCalc):
        super().__init__()
        self.node_calc = node_calc
        self.coord_system = CoordinateSystem.GEO

    def create_position(self, point: str, dt: datetime) -> BasePosition:
        dt = dt.replace(tzinfo=pytz.utc)
        if point in PLANETS:
            return self._geo(point, dt)
        elif point == NN:
            return self._north_node(dt)
        elif point == SN:
            return self._south_node(dt)
        else:
            raise (ValueError(f"{point} not supported"))

    def _geo(self, planet_name: str, dt: datetime) -> BasePosition:
        lon, lat, speed = swe_api.get_ecliptic_position(planet_name, dt)
        ra, dec = swe_api.get_equatorial_position(planet_name, dt)
        lon, lat, speed, ra, dec = to_degree(lon, lat, speed, ra, dec)
        return BasePosition(
            dt, self.coord_system, planet_name, lon, lat, speed, ra, dec
        )

    def _north_node(self, dt: datetime) -> BasePosition:
        pos = self._geo(self.node_calc.swe_flag(), dt)
        pos.point = NN
        return pos

    def _south_node(self, dt: datetime) -> BasePosition:
        nn = self._north_node(dt)
        lon = (nn.lon.decimal + 180.0) % 360
        lat = 0
        speed = nn.speed.decimal
        ra = (nn.ra.decimal + 12.0) % 24.0
        dec = -nn.dec.decimal
        lon, lat, speed, ra, dec = to_degree(lon, lat, speed, ra, dec)
        return BasePosition(dt, self.coord_system, SN, lon, lat, speed, ra, dec)

    def create_angular(self, point: str, dt: datetime, lon: float) -> BasePosition:
        lon, lat, speed, ra, dec = to_degree(lon, 0, 0, 0, 0)

        return BasePosition(dt, self.coord_system, point, lon, lat, speed, ra, dec)
