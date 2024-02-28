from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.core.events.astro_event import DirectionChange
from astrotoolz.core.points import ALL_POINTS, MOON, NN, SN, SUN
from astrotoolz.timeline.aspect_config import AspectsConfig


@dataclass
class TimelineConfig:
    coordinate_system: CoordinateSystem
    start_date: datetime
    end_date: datetime
    interval_minutes: int
    points: List[str]
    node_calc: Optional[NodeCalc]
    events: Optional[List[type]]
    aspects: Optional[List[AspectsConfig]]

    def __init__(
        self,
        coordinate_system: CoordinateSystem,
        start_date: datetime,
        end_date: datetime,
        interval_minutes: int,
        points: List[str],
        node_calc: Optional[NodeCalc] = None,
        events: Optional[List[type]] = [],
        aspects: Optional[List[AspectsConfig]] = [],
    ):
        self.coordinate_system = coordinate_system
        self.start_date = start_date
        self.end_date = end_date
        self.interval_minutes = interval_minutes
        self.points = [p.lower() for p in points] if points is not None else []
        self.node_calc = node_calc
        self.events = events
        self.aspects = aspects

    def validate(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")

        if self.interval_minutes < 1:
            raise ValueError("Interval must be at least 1 minute")

        for p in self.points:
            if p not in ALL_POINTS:
                raise ValueError(f"{p} is not a valid point")

        if not self.points:
            raise ValueError("No valid points found")

        if self.coordinate_system == CoordinateSystem.HELIO:
            self.validate_helio()

        if self.coordinate_system == CoordinateSystem.GEO:
            self.validate_geo()

        if not self.events and not self.aspects:
            raise ValueError("At least one event or aspects must be specified")

        for aspc in self.aspects:
            aspc.validate()

    def validate_helio(self):
        for p in self.points:
            if p in [SUN, MOON, NN, SN]:
                raise ValueError(f"{p} is not a valid source for Helio")

        for aspc in self.aspects:
            for t in aspc.targets:
                if t in [SUN, MOON, NN, SN]:
                    raise ValueError(f"{t} is not a valid angle target for Helio")

        if DirectionChange in self.events:
            raise ValueError(f"{DirectionChange} is not valid for Helio")

    def validate_geo(self):
        if MOON in self.points and self.node_calc is None:
            raise ValueError(f"Node calculation must be specified for {MOON}")
