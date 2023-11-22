from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime as dt
from core.angle_factory import AngleFactory
from core.enums import AspectType, CoordinateSystem
from core.position_factory import PositionFactory
from events.aspect_finder import AspectFinder
from objects.points import get_all_default_angle_targets
from events.astro_event import AstroEvent, DecanChange, DirectionChange, NakshatraChange, Progression, SignChange, TermChange
from events.zodiacal_event_factory import ZodiacalEventFactory
from objects.orb_map import OrbMap
from objects.points import ALL_POINTS, MEAN_NODE, POINTS_NO_MOON


DEFAULT_ASPECTS = [
    AspectType.CONJUNCTION,
    AspectType.OPPOSITION,
    AspectType.SQUARE,
    AspectType.TRINE,
    AspectType.SEXTILE,
    AspectType.INCONJUNCT,
    AspectType.QUINTILE,
]

DEFAULT_ZODIACAL_EVENTS = [SignChange, DecanChange,
                           TermChange, NakshatraChange, DirectionChange, Progression]


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

    @classmethod
    def default_no_moon(
        cls,
        start: dt,
        end: dt,
        aspects: List[AspectType]=DEFAULT_ASPECTS,
        zodiacal_events :List[type]=DEFAULT_ZODIACAL_EVENTS,
    ) -> "TimelineConfig":

        return TimelineConfig.default(start, end, POINTS_NO_MOON)

    @classmethod
    def default(
        cls,
        start: dt,
        end: dt,
        points=ALL_POINTS,
        angle_targets={},
        aspects=DEFAULT_ASPECTS,
        zodiacal_events=DEFAULT_ZODIACAL_EVENTS,
    ) -> "TimelineConfig":

        if not angle_targets:
            angle_targets = get_all_default_angle_targets()
        else:
            cls._check_targets(points, angle_targets)

        position_factory = PositionFactory(MEAN_NODE)
        angle_factory = AngleFactory(position_factory, angle_targets)
        orb_map = OrbMap.orb_map(0.001)
        aspect_finder = AspectFinder(
            orb_map, aspects) if len(aspects) > 0 else None
        zodiacal_event_factory = ZodiacalEventFactory(
            zodiacal_events) if len(zodiacal_events) > 0 else None

        return TimelineConfig(
            start,
            end,
            1,
            points,
            position_factory,
            angle_factory,
            zodiacal_event_factory,
            aspect_finder,
        )

    @classmethod
    def _check_targets(cls, points: List[str], angle_targets: Dict[str, List[str]]):
        for point in points:
            if point not in angle_targets:
                raise ValueError(f"Point {point} not found in angle targets")
