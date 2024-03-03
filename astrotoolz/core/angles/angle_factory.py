from typing import Callable, Dict, List

from astrotoolz.core.angles.angle import Angle
from astrotoolz.core.positions.base_position import BasePosition
from astrotoolz.core.positions.factory.position_factory import PositionFactory
from astrotoolz.core.zodiac.mapped_position import MappedPosition
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.util.logger_base import LoggerBase


class AngleFactory(LoggerBase):

    def __init__(
        self, position_factory: PositionFactory, position_mapper: PositionMapper
    ):
        super().__init__()
        self.position_factory = position_factory
        self.position_mapper = position_mapper

    def create_angles_dict(
        self, mps: Dict[str, List[BasePosition]], targets: Dict[str, List[Angle]]
    ) -> Dict[str, List[Angle]]:
        angles_list = self.create_angles_list(mps, targets)

        angles_dict = {angle.source.point: [] for angle in angles_list}
        for angle in angles_list:
            angles_dict[angle.source.point].append(angle)
        return angles_dict

    def create_angles_list(
        self,
        bps: Dict[str, List[BasePosition]],
        targets: Dict[str, List[str]],
    ) -> List[Angle]:
        angles = []
        for p, bp_list in bps.items():
            current_targets = targets[p]

            self._logger.info(f"Generating angles for {p}")

            for source_bp in bp_list:
                for t in current_targets:
                    if t == source_bp.point:
                        continue

                    target_bp = self.position_factory.create_position(t, source_bp.dt)
                    angle = Angle(source_bp, target_bp)
                    angles.append(angle)

        return angles
