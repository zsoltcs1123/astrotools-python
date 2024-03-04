from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

from astrotoolz.core.points import LUMINARIES


class OrbCalculator(ABC):

    @abstractmethod
    def calculate_orb(
        self, point: Optional[str] = None, angle: Optional[int] = None
    ) -> float:
        pass


class StaticOrbCalculator(OrbCalculator):

    def __init__(self, orb_value):
        self.orb_value = orb_value

    def calculate_orb(
        self, point: Optional[str] = None, angle: Optional[int] = None
    ) -> float:
        return self.orb_value


class DynamicOrbCalculator(OrbCalculator):

    def __init__(self, orb_map: Optional[Dict[Tuple[str, int], float]] = None):
        self.orb_map = orb_map

    def calculate_orb(
        self, point: Optional[str] = None, angle: Optional[int] = None
    ) -> float:

        if point is None or angle is None:
            raise ValueError("Point and angle must be provided")

        if self.orb_map is None:
            return self.default_orbs(point, angle)

    def default_orbs(self, point: str, angle: int) -> float:
        if angle in [30, 60, 300, 330]:
            return 6 if point in LUMINARIES else 4
        elif angle in [0, 90, 120, 180, 360]:
            return 10 if point in LUMINARIES else 8
        elif angle in [150, 210]:
            return 5 if point in LUMINARIES else 3
        else:
            return 8 if point in LUMINARIES else 6
