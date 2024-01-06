from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from core.enums import CoordinateSystem, NodeCalc


@dataclass
class AspectsConfig:
    angle: int
    family: bool


@dataclass
class TimelineConfig:
    coordinate_system: CoordinateSystem
    start_date: datetime
    end_date: datetime
    interval_minutes: int
    points: List[str]
    node_calc: NodeCalc
    events: List[type]
    aspects: Optional[AspectsConfig] = field(default=None)

    def validate(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")

        if self.interval_minutes < 1:
            raise ValueError("Interval must be at least 1 minute")

        if self.events.__len__ == 0 and self.aspects is None:
            raise ValueError("At least one event or aspects must be specified")
