from dataclasses import dataclass
from typing import List, Optional

from astrotoolz.core.events.orb_calculator import OrbCalculator
from astrotoolz.core.points import ALL_POINTS, SUN


@dataclass
class AspectsConfig:
    angle: int
    family: bool
    orb_calculator: OrbCalculator
    targets: Optional[List[str]]

    def __init__(
        self,
        angle: int,
        family: bool,
        orb_calculator: OrbCalculator,
        targets: Optional[List[str]] = None,
    ):
        self.angle = angle
        self.family = family
        self.orb_calculator = orb_calculator
        self.targets = [t.lower() for t in targets] if targets is not None else []

    def validate(self):
        for t in self.targets:
            if t not in ALL_POINTS and t != SUN:
                raise ValueError(f"{t} is not a valid target")

    def generate_asp_family(self) -> List[float]:
        root = self.angle if self.angle != 0 else 360
        return [multiple for multiple in range(0, 361, root)]
