from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime as dt
from core.enums import AspectType
from events.aspects.aspect import DEFAULT_ASPECTS
from core.objects.points import get_default_angle_targets
from events.zodiacal.astro_event import (
    DecanChange,
    DirectionChange,
    NakshatraChange,
    TropicalProgression,
    TropicalSignChange,
    TermChange,
)
from events.aspects.orb_map import OrbMap
from core.objects.points import ALL_POINTS, MEAN_NODE, POINTS_NO_MOON


DEFAULT_ZODIACAL_EVENTS = [
    TropicalSignChange,
    DecanChange,
    TermChange,
    NakshatraChange,
    DirectionChange,
    TropicalProgression,
]


@dataclass
class TimelineConfig:
    start: dt
    end: dt
    interval_minutes: int
    points: List[str]
    node_calc: str
    zodiacal_events: List[type]
    aspects: List[AspectType]
    angle_targets: Dict[str, List[str]]
    orb_map: OrbMap

    @classmethod
    def default_no_moon(
        cls,
        start: dt,
        end: dt,
        zodiacal_events: List[type] = DEFAULT_ZODIACAL_EVENTS,
    ) -> "TimelineConfig":
        return TimelineConfig.default(start, end, POINTS_NO_MOON, zodiacal_events)

    @classmethod
    def default(
        cls,
        start: dt,
        end: dt,
        points: List[str] = ALL_POINTS,
        zodiacal_events: List[type] = DEFAULT_ZODIACAL_EVENTS,
        angle_targets: Dict[str, List[str]] = {},
    ) -> "TimelineConfig":
        if not angle_targets:
            angle_targets = cls.get_all_default_angle_targets(points)
        else:
            cls._check_targets(points, angle_targets)

        return TimelineConfig(
            start,
            end,
            1,
            points,
            MEAN_NODE,
            zodiacal_events,
            DEFAULT_ASPECTS,
            angle_targets,
            OrbMap.from_float(0.001),
        )

    @classmethod
    def _check_targets(cls, points: List[str], angle_targets: Dict[str, List[str]]):
        for point in points:
            if point not in angle_targets:
                raise ValueError(f"Point {point} not found in angle targets")

    @classmethod
    def get_all_default_angle_targets(cls, points: List[str]) -> Dict[str, List[str]]:
        targets = {}
        for p in points:
            targets[p] = get_default_angle_targets(p)
        return targets
