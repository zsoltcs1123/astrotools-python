from typing import List
from dataclasses import dataclass
from datetime import datetime
from core.angle_factory import generate_angles_from_mps
from core.enums import CoordinateSystem
from core.position_factory import create_position
from objects.points import get_default_angle_targets
from zodiac.mapped_position import MappedPosition


@dataclass
class AngleTable:
    def __init__(
        self, dt: datetime, planets: List[str], coord_system: CoordinateSystem
    ):
        bps = [create_position(p, dt, coord_system) for p in planets]
        self.mps = MappedPosition.from_planetary_positions(bps)
        self.angles = generate_angles_from_mps(self.mps, get_default_angle_targets)
