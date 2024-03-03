from datetime import datetime, timezone

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.points import MOON, NN, SN, SUN
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.util.common import to_degree


class HelioFactory(PositionFactory):

    def create_position(self, point, dt: datetime) -> BasePosition:
        dt = dt.replace(tzinfo=timezone.utc)
        if point in [SUN, MOON, NN, SN]:
            raise (ValueError(f"{point} not supported"))
        else:
            return self._helio(point, dt)

    def _helio(self, point: str, dt: datetime) -> BasePosition:
        lon, lat, speed = swe_api.get_helio_position(point, dt)
        lon, lat, speed = to_degree(lon, lat, speed)
        return BasePosition(
            dt, CoordinateSystem.HELIO, point, lon, lat, speed, None, None
        )

    def create_angular(self, point, dt: datetime, lon: float) -> BasePosition:
        raise (ValueError(f"{point} not supported"))
