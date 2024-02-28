from datetime import datetime, timezone

import astrotoolz.core.ephemeris.swisseph_api as swe_api
from astrotoolz.core.points import MOON, NN, SN, SUN
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.positions.helio_position import HelioPosition
from astrotoolz.util.common import to_degree


class HelioFactory(PositionFactory):

    def create_position(self, point, dt: datetime) -> HelioPosition:
        dt = dt.replace(tzinfo=timezone.utc)
        if point in [SUN, MOON, NN, SN]:
            raise (ValueError(f"{point} not supported"))
        else:
            return self._helio(point, dt)

    def _helio(self, point: str, dt: datetime) -> HelioPosition:
        lon, lat, speed = swe_api.get_helio_position(point, dt)
        lon, lat, speed = to_degree(lon, lat, speed)
        return HelioPosition(dt, point, lon, lat, speed)
