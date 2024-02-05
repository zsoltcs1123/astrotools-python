from typing import List

from core.enums import CoordinateSystem
from core.objects.points import ANGULARS, MOON, NN, NODES, PLANETS, PLANETS_MAP, SUN


class AngleTargetCalculator:
    def __init__(self, coordinate_system: str):
        self.coordinate_system = coordinate_system

    def calculate(self, point: str) -> List[str]:
        if self.coordinate_system == CoordinateSystem.GEO:
            return self._calculate_geo_targets(point)
        else:
            return self._calculate_helio_targets(point)

    def _calculate_geo_targets(point: str) -> List[str]:
        if point == SUN:
            return list(PLANETS_MAP.keys()) + [NN]
        elif point == MOON:
            return list(PLANETS_MAP.keys()) + [SUN] + [NN]
        elif point in NODES:
            return []
        elif point in ANGULARS:
            return PLANETS + NODES
        else:
            return [k for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[point]] + [NN]

    def _calculate_helio_targets(point: str) -> List[str]:
        if point in PLANETS:
            return [k for k, v in PLANETS_MAP.items() if v > PLANETS_MAP[point]]
        else:
            return []
