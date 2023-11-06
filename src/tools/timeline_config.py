from typing import List
from dataclasses import dataclass
from datetime import datetime as dt
from core.angle_factory import AngleFactory
from core.enums import AspectType, CoordinateSystem
from core.position_factory import PositionFactory
from events.aspect_finder import AspectFinder
from events.astro_event import DecanChange, DirectionChange, SignChange, TermChange
from events.zodiacal_event_factory import ZodiacalEventFactory
from objects.orb_map import OrbMap
from objects.points import MEAN_NODE, POINTS_NO_MOON


DEFAULT_ASPECTS = [
    AspectType.CONJUNCTION,
    AspectType.OPPOSITION,
    AspectType.SQUARE,
    AspectType.TRINE,
    AspectType.SEXTILE,
    AspectType.INCONJUNCT,
    AspectType.QUINTILE,
]

DEFAULT_ZODIACAL_EVENTS = [SignChange, DecanChange, TermChange, DirectionChange]


@dataclass
class TimelineConfig:
    start: dt
    end: dt
    interval_minutes: int
    points: List[str]
    position_factory: PositionFactory
    angle_factory: AngleFactory
    zodiacal_event_factory: ZodiacalEventFactory = None
    aspect_finder: AspectFinder = None
    coordinate_system = CoordinateSystem.GEO

    @staticmethod
    def default_no_moon(start: dt, end: dt) -> "TimelineConfig":
        position_factory = PositionFactory(MEAN_NODE)
        angle_factory = AngleFactory(position_factory)
        orb_map = OrbMap.orb_map(0.001)
        aspect_finder = AspectFinder(orb_map, DEFAULT_ASPECTS)
        zodiacal_event_factory = ZodiacalEventFactory(DEFAULT_ZODIACAL_EVENTS)

        return TimelineConfig(
            start,
            end,
            1,
            POINTS_NO_MOON,
            position_factory,
            angle_factory,
            zodiacal_event_factory,
            aspect_finder,
        )
