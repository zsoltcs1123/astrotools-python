from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from core.base_position import BasePosition
from core.geo_position import GeoPosition
from core.enums import CoordinateSystem

from core.position_factory import create_helio_position, create_position
from objects.points import ASC, MC, MERCURY, MOON, VENUS


def generate_square_outs(
    start_time: datetime,
    degrees: float,
    planets: List[str],
    coord_system: CoordinateSystem,
) -> Dict[str, Tuple]:
    square_outs = {}
    for p in planets:
        bp = (
            create_position(p, start_time)
            if coord_system == CoordinateSystem.GEO
            else create_helio_position(p, start_time)
        )
        square_out = _find_square_out(bp, degrees, _get_interval(p))
        square_outs[p] = (bp, square_out)

    return square_outs


def _find_square_out(
    starting_position: BasePosition, degrees: float, interval_hours: int
) -> BasePosition:
    current_time = starting_position.dt
    cum_degrees = 0
    pp = starting_position
    creator_func = (
        create_position if isinstance(pp, GeoPosition) else create_helio_position
    )

    while True:
        current_time += timedelta(hours=interval_hours)
        np = creator_func(starting_position.point, current_time)
        cum_degrees += abs(np.lon.decimal - pp.lon.decimal)

        if cum_degrees >= degrees:
            return np

        pp = np


def _get_interval(planet: str) -> int:
    if planet in [ASC, MC, MOON, MERCURY, VENUS]:
        return 1
    else:
        return 24
