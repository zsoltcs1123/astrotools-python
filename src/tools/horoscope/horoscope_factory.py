from datetime import datetime
from typing import List
from core.angle_factory import AngleFactory
from core.position_factory import PositionFactory
from events.aspect_finder import AspectFinder
from objects.orb_map import OrbMap
from objects.points import get_all_default_angle_targets
from tools.horoscope.horoscope import Horoscope
from tools.horoscope.horoscope_config import HoroscopeConfig
from util.interval import calculate_intervals


def create_horoscope(dt: datetime, config: HoroscopeConfig) -> Horoscope:
    position_factory = PositionFactory(config.node_calc)

    if config.aspects:
        angle_targets = get_all_default_angle_targets()
        angle_factory = AngleFactory(position_factory, angle_targets)
        orb_map = OrbMap.default()
        aspect_finder = AspectFinder(orb_map, config.aspects)
        return Horoscope(dt, config, position_factory, angle_factory, aspect_finder)
    else:
        return Horoscope(dt, config, position_factory, None, None)


def create_horoscopes(
    start: datetime, end: datetime, interval_minutes: int, config: HoroscopeConfig
) -> List[Horoscope]:
    dts = calculate_intervals(start, end, interval_minutes)

    return [create_horoscope(dt, config) for dt in dts]
