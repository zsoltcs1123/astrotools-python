from datetime import datetime, timezone
from typing import List

import core.ephemeris.swisseph_api as swe_api
from core.objects.points import MOON, NN, SN, SUN
from core.positions.helio_position import HelioPosition
from util.common import _to_degree
from util.interval import calculate_intervals


class HelioFactory:
    def create_positions(
        self, point: str, start: datetime, end: datetime, interval_minutes: int
    ) -> List[HelioPosition]:
        self._logger.debug(
            f"Generating positions for config: {point}, {start}, {end}, {interval_minutes}"
        )
        dts = calculate_intervals(start, end, interval_minutes)
        return [self.create_position(point, dt) for dt in dts]

    def create_position(self, point, dt: datetime) -> HelioPosition:
        dt = dt.replace(tzinfo=timezone.utc)
        if point in [SUN, MOON, NN, SN]:
            raise (ValueError(f"{point} not supported"))
        else:
            return self._helio(point, dt)

    def _helio(self, point: str, dt: datetime) -> HelioPosition:
        lon, lat, speed = swe_api.get_helio_position(point, dt)
        lon, lat, speed = _to_degree(lon, lat, speed)
        return HelioPosition(dt, point, lon, lat, speed)
