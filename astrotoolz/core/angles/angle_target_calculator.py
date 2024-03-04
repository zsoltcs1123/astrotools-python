from typing import Dict, List, Optional

from astrotoolz.core.enums import CoordinateSystem
from astrotoolz.core.points import ANGULARS, MOON, NN, NODES, PLANETS, PLANETS_MAP, SUN
from astrotoolz.util.logger_base import LoggerBase


class AngleTargetCalculator(LoggerBase):

    def __init__(self, coordinate_system: CoordinateSystem):
        super().__init__()
        self.coordinate_system = coordinate_system

    def calculate(
        self, point: str, include_targets: Optional[List[str]] = None
    ) -> List[str]:
        targets = []
        if self.coordinate_system == CoordinateSystem.GEO:
            targets = self._calculate_geo_targets(point)
        else:
            targets = self._calculate_helio_targets(point)

        if include_targets:
            targets = [target for target in targets if target in include_targets]

        self._logger.debug(f"Identified angle targets for {point}: {targets}")
        return targets

    def calculate_dict(
        self, points: List[str], include_targets: Optional[List[str]] = None
    ) -> Dict[str, List[str]]:
        return {p: self.calculate(p, include_targets) for p in points}

    @staticmethod
    def _calculate_geo_targets(point: str) -> List[str]:
        if point == SUN:
            return list(PLANETS_MAP.keys()) + [NN, MOON]
        elif point == MOON:
            return list(PLANETS_MAP.keys()) + [SUN] + [NN]
        elif point in NODES:
            return []
        elif point in ANGULARS:
            return PLANETS + [NN]
        else:
            return [k for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[point]] + [NN]

    @staticmethod
    def _calculate_helio_targets(point: str) -> List[str]:
        if point in PLANETS:
            return [k for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[point]]
        else:
            return []
