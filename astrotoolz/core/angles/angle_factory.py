from typing import Callable, Dict, List

from astrotoolz.core.angles.angle import Angle
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
        self, mps: List[MappedPosition], target_selector: Callable[[str], List[str]]
    ) -> Dict[str, List[Angle]]:
        angles = {}
        for mp in mps:
            targets = target_selector(mp.point)

            angles[mp.point] = []

            for t in targets:
                target_mp = next((p for p in mps if p.point == t), None)
                if target_mp is not None:
                    angle = Angle(mp, target_mp)
                    angles[mp.point].append(angle)

        return angles

    def create_angles_list(
        self,
        mps: Dict[str, List[MappedPosition]],
        targets: Dict[str, List[str]],
    ) -> List[Angle]:
        angles = []
        for p, mp_list in mps.items():
            current_targets = targets[p]

            self._logger.info(f"Generating angles for {p}")

            for source_mp in mp_list:
                for t in current_targets:
                    if t == source_mp.point:
                        continue

                    target_bp = self.position_factory.create_position(t, source_mp.dt)
                    target_mp = self.position_mapper.map_position(target_bp)
                    angle = Angle(source_mp, target_mp)
                    angles.append(angle)

        return angles
