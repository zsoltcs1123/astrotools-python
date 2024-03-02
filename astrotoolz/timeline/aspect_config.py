from dataclasses import dataclass
from typing import List, Optional

from astrotoolz.core.points import ALL_POINTS, SUN


@dataclass
class AspectsConfig:
    angle: int
    family: bool
    orb: float
    targets: Optional[List[str]]

    def __init__(
        self, angle: int, family: bool, orb: float, targets: Optional[List[str]] = None
    ):
        self.angle = angle
        self.family = family
        self.orb = orb
        self.targets = [t.lower() for t in targets] if targets is not None else []

    def validate(self):
        for t in self.targets:
            if t not in ALL_POINTS and t != SUN:
                raise ValueError(f"{t} is not a valid target")

        if self.orb <= 0:
            raise ValueError("Orb must be greater than 0")
