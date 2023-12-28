from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime as dt
from core.enums import AspectType
from events.aspects.aspect import DEFAULT_ASPECTS
from core.objects.points import get_default_angle_targets
from events.zodiacal.astro_event import (
    DecanChange,
    DeclinationExtreme,
    DirectionChange,
    LatitudeExtreme,
    NakshatraChange,
    PhaseExtreme,
    SpeedExtreme,
    TropicalProgression,
    TropicalSignChange,
    TermChange,
    VedicSignChange,
)
from events.aspects.orb_map import OrbMap
from core.objects.points import ALL_POINTS, MEAN_NODE, POINTS_NO_MOON

ZODIACAL_EVENTS = [
    TropicalSignChange,
    DecanChange,
    TermChange,
    NakshatraChange,
    VedicSignChange,
    TropicalProgression,
    DirectionChange,
]
EXTREME_EVENTS = [DeclinationExtreme, LatitudeExtreme, SpeedExtreme]


DEFAULT_ASTRO_EVENTS = ZODIACAL_EVENTS + EXTREME_EVENTS


@dataclass
class TimelineConfig:
    start: dt
    end: dt
    interval_minutes: int
    points: List[str]
    astro_events: List[type]
    aspects: List[AspectType]
    angle_targets: Dict[str, List[str]]
    orb_map: OrbMap
    node_calc: str

    @classmethod
    def default_no_moon(
        cls,
        start: dt,
        end: dt,
        astro_events: List[type] = DEFAULT_ASTRO_EVENTS,
    ) -> "TimelineConfig":
        return TimelineConfig.default(start, end, 1, POINTS_NO_MOON, astro_events)

    @classmethod
    def default(
        cls,
        start: dt,
        end: dt,
        interval_minutes: int = 1,
        points: List[str] = ALL_POINTS,
        astro_events: List[type] = DEFAULT_ASTRO_EVENTS,
        aspects: List[AspectType] = DEFAULT_ASPECTS,
        angle_targets: Dict[str, List[str]] = {},
    ) -> "TimelineConfig":
        if not angle_targets:
            angle_targets = cls.get_all_default_angle_targets(points)
        else:
            cls._check_targets(points, angle_targets)

        return TimelineConfig(
            start,
            end,
            interval_minutes,
            points,
            astro_events,
            aspects,
            angle_targets,
            OrbMap.from_float(0.001),
            MEAN_NODE,
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
