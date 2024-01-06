from dataclasses import dataclass
from datetime import datetime

from core.enums import CoordinateSystem, NodeCalc


@dataclass
class PositionFactoryConfig:
    coordinate_system: CoordinateSystem
    point: str
    start: datetime
    end: datetime
    interval_minutes: int
    node_calc: NodeCalc
