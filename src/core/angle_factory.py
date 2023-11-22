
from typing import Dict, List
from datetime import datetime
from core.angle import Angle
from core.position_factory import PositionFactory
from util.interval import calculate_intervals


class AngleFactory:
    def __init__(self, position_factory: PositionFactory, angle_targets: Dict[str, List[str]] = {}):
        self.position_factory = position_factory
        self.angle_targets = angle_targets

    def get_single_angle(self, source_point: str, target_point: str, dt: datetime) -> Angle:
        source = self.position_factory.create_position(source_point, dt)
        target = self.position_factory.create_position(target_point, dt)

        return Angle(source, target)

    def get_multiple_angles(self, source_point: str, target_points: List[str], dt: datetime) -> List[Angle]:
        return [self.get_single_angle(source_point, target_point, dt) for target_point in target_points]

    def get_single_angle_in_range(self, source_point: str, target_point: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
        datetimes = calculate_intervals(start, end, interval)
        return [self.get_single_angle(source_point, target_point, t) for t in datetimes]

    def get_multiple_angles_in_range(self, source_point: str, start: datetime, end: datetime, interval: int) -> List[Angle]:
        return [angle for target_point in self.angle_targets[source_point] for angle in self.get_single_angle_in_range(source_point, target_point, start, end, interval)]
