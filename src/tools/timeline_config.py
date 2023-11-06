from typing import List
from dataclasses import dataclass
from datetime import datetime as dt
from core.enums import CoordinateSystem
from core.position_factory import PositionFactory
from events.aspect import DEFAULT_ASPECTS
from events.aspect_finder import AspectFinder
from objects.orb_map import OrbMap
from objects.points import POINTS_NO_MOON


@dataclass
class TimelineConfig:
    start: dt
    end: dt
    interval_minutes: int
    points: List[str]
    position_factory: PositionFactory
    aspect_finder: AspectFinder = None
    coordinate_system = CoordinateSystem.GEO

    @staticmethod
    def default_no_moon(start: dt, end: dt) -> "TimelineConfig":
        position_factory = PositionFactory()
        orb_map = OrbMap.orb_map(0.001)
        aspect_finder = AspectFinder(orb_map, DEFAULT_ASPECTS)

        return TimelineConfig(start, end, 1, POINTS_NO_MOON, position_factory, aspect_finder)
    

