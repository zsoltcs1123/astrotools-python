from datetime import datetime

import pytz

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.enums import NodeCalc
from astrotoolz.core.points import NN, PLANETS, SN
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.positions.geo_position import GeoPosition
from astrotoolz.util.common import to_degree


class GeoFactory(PositionFactory):
    node_calc: NodeCalc

    def __init__(self, node_calc: NodeCalc):
        super().__init__()
        self.node_calc = node_calc

    def create_position(self, point: str, dt: datetime) -> GeoPosition:
        dt = dt.replace(tzinfo=pytz.utc)
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
        lon, lat, speed, ra, dec = to_degree(lon, lat, speed, ra, dec)
        return GeoPosition(dt, planet_name, lon, lat, speed, ra, dec)

    def _north_node(self, dt: datetime) -> GeoPosition:
        pos = self._geo(self.node_calc.swe_flag(), dt)
        pos.point = NN
        return pos

    def _south_node(self, dt: datetime) -> GeoPosition:
        nn = self._north_node(dt)
        lon = (nn.lon.decimal + 180.0) % 360
        lat = 0
        speed = nn.speed.decimal
        ra = (nn.ra.decimal + 12.0) % 24.0
        dec = -nn.dec.decimal
        lon, lat, speed, ra, dec = to_degree(lon, lat, speed)
        return GeoPosition(dt, SN, lon, lat, speed, ra, dec)
