from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from astrotoolz.core.enums import CoordinateSystem, NodeCalc
from astrotoolz.core.events.astro_event import DirectionChange
from astrotoolz.core.points import ALL_POINTS, MOON, NN, SN, SUN


@dataclass
class AspectsConfig:
    angle: int
    family: bool
    orb: float
    targets: Optional[List[str]] = field(default_factory=list)

    def validate(self):
        if not all(target in ALL_POINTS for target in self.targets):
            raise ValueError("Invalid targets")  # TODO specify which


@dataclass
class TimelineConfig:
    coordinate_system: CoordinateSystem
    start_date: datetime
    end_date: datetime
    interval_minutes: int
    points: List[str]
    node_calc: NodeCalc
    events: Optional[List[type]] = field(default_factory=list)
    aspects: Optional[List[AspectsConfig]] = field(default_factory=list)

    def validate(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")

        if self.interval_minutes < 1:
            raise ValueError("Interval must be at least 1 minute")

        if not all(point in ALL_POINTS for point in self.points):
            raise ValueError("Invalid points")  # TODO specify which

        if self.coordinate_system == CoordinateSystem.HELIO:
            self.process_helio()

        if not self.points:
            raise ValueError("No valid points found")

        if not self.events and not self.aspects:
            raise ValueError("At least one event or aspects must be specified")

        for aspc in self.aspects:
            aspc.validate()

    def process_helio(self):
        self.points = [
            point for point in self.points if point not in [SUN, MOON, NN, SN]
        ]

        self.events = [event for event in self.events if event not in [DirectionChange]]
